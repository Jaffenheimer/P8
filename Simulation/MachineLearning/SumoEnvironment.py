import gymnasium as gym
import numpy as np
import traci
import math
from os import path
from Constants import MAX_STEPS, SUMO_INIT_STEPS, REWARD_THRESHOLD, SEED


class SumoEnv(gym.Env):
    def __init__(self):
        self.close()

        traci.start(
            ["sumo", "-c", path.abspath("../P8-Mobility/Simulation/SUMO/algorithm/algorithm.sumocfg"), "--seed", str(SEED)])
        ## VARIABLES ##
        self.bus_num = 10
        self.current_step = 0
        self.max_steps = MAX_STEPS+1
        bus_speed_max = 13.9  # 13.9 m/s = 50 km/h

        ## SUMO VARIABLES ##
        self.bus_stop_positions = [
            [123, 974, 1872, 2764], [123, 827, 1742, 2702, 3592]]
        self.bus_locations = {"-overlap": "123", "-R2": "259", "-R1": "125",
                              "-R0": "267", "-L3": "117", "-L2": "110", "-L1": "123", "-L0": "120"}
        self.bus_ids = ["bus_r_0_0", "bus_r_1_0", "bus_r_0_1", "bus_r_1_1",
                        "bus_r_0_2", "bus_r_1_2", "bus_r_0_3", "bus_r_1_3", "bus_r_0_4", "bus_r_1_4"]
        self.route_lengths = [3591, 4697]
        self.overlap_lane_length = 706.59
        self.wait_time = 0
        self.previous_speeds_m_s = [0]*self.bus_num

        ## GYM INITIALIZATIONS ##

        # actions: [b0(r0), (...), b0(r1), (...)] # each action is either -1 = slow down, 0 = keep speed, 1 = speed up
        self.action_space = gym.spaces.Box(low=np.array([np.float32(-1)]*self.bus_num), high=np.array(
            [np.float32(1)]*self.bus_num), shape=(self.bus_num,), dtype=np.float32)

        # state: [avg_wait_time, avg_people_at_busstops, b0(r0)_speed, b0(r0)_pos, (...), b0(r1)_speed, b0(r1)_pos, (...)]
        wait_time_max = 100000
        average_people_at_busstops_max = 10000
        low_obs = np.zeros([1 + 1 + 2*self.bus_num])
        high_obs = np.array([wait_time_max] + [average_people_at_busstops_max] + [bus_speed_max, self.route_lengths[0]]
                            * 5 + [bus_speed_max, self.route_lengths[1]]*5)
        self.observation_space = gym.spaces.Box(
            low=low_obs, high=high_obs, shape=(1 + 1 + 2*self.bus_num,), dtype=np.float32)

        # Run simulation for SUMO_INIT_STEPS to initialize the simulation with stable wait time

        for _ in range(SUMO_INIT_STEPS):
            self.sumo_step()

    # GYM FUNCTIONS
    def reset(self, seed=None, options=None):
        traci.close()
        self.wait_time = 0
        self.current_step = 0
        self.previous_speeds_m_s = [0]*self.bus_num
        traci.start(
            ["sumo", "-c", path.abspath("../P8-Mobility/Simulation/SUMO/algorithm/algorithm.sumocfg"), "--seed", str(SEED)])
        return np.concatenate(([self.wait_time], np.zeros(1+2 * self.bus_num))).astype(np.float32)[:22], {}

    def even_probability(self, action_value):
        if action_value < -0.33:
            return -1
        elif action_value > 0.33:
            return 1
        else:
            return 0

    def accelerate_km_h(self, speed):
        return min(50, speed + (-0.0125*(speed**2)+(0.346428*speed)+13.9286))

    def decelerate_km_h(self, speed):
        return speed - (0.25 * speed)

    def step(self, action):
        try:
            next_state = self.sumo_step()

            # set action for each bus: -1 = slow down, 0 = keep speed, 1 = speed up
            vehicles_length = len(traci.vehicle.getIDList())

            for i, action_value in enumerate(action):
                if i >= vehicles_length:
                    break

                bus_id = self.bus_ids[i]
                bus_distance_driven = traci.vehicle.getDistance(bus_id)

                if np.sign(bus_distance_driven) == -1:
                    break  # if bus hasnt driven yet, skip

                # round action to -1, 0 or 1, since it is a continuous action space (float)
                bus_action = self.even_probability(action_value)
                bus_route = traci.vehicle.getRouteID(bus_id)
                bus_route_index = 0 if bus_route == "r_0" else 1
                bus_position = round(bus_distance_driven %
                                     (self.route_lengths[bus_route_index]), 3)
                nearest_bus_stop_position = self._find_nearest(
                    self.bus_stop_positions[bus_route_index], bus_position)
                bus_speed_m_s = traci.vehicle.getSpeed(bus_id)
                bus_speed_km_h = bus_speed_m_s*3.6

                # interval for bus stop position where speed is not changed
                bus_stop_interval = [-22, 3]
                new_speed_m_s = bus_speed_m_s
                # if bus should keep speed, set speed to current speed if the previous speed is 0, otherwise to previous speed
                if bus_action == 0:
                    if self.previous_speeds_m_s[i] not in [0.0, 0]:
                        new_speed_m_s = self.previous_speeds_m_s[i]
                    # smoothly changes to new speed over 1 time step
                    traci.vehicle.slowDown(bus_id, new_speed_m_s, 1)
                # accelerate/decelerate if bus is not within the bus stop position interval
                elif (not (bus_position > nearest_bus_stop_position + bus_stop_interval[0] and bus_position < nearest_bus_stop_position + bus_stop_interval[1])):
                    if bus_action == -1:
                        new_speed_m_s = self.decelerate_km_h(
                            bus_speed_km_h) / 3.6
                    elif bus_action == 1:
                        # if too close to the next bus accelerate=min(accelerate, speed of next bus), otherwise accelerate normally
                        new_speed_m_s = self.accelerate_km_h(
                            bus_speed_km_h) / 3.6

                    traci.vehicle.slowDown(bus_id, new_speed_m_s, 1)

                # store previous speed for keep speed action in next step
                self.previous_speeds_m_s[i] = new_speed_m_s

            # reward are given if the new waiting time is strictly lower, otherwise punished
            reward = 1 if next_state[0] <= self.wait_time else -1

            # set the wait time to the current wait time
            self.wait_time = next_state[0]

            # check if done
            self.current_step += 1
            done = False
            if (self.current_step >= self.max_steps-1):
                done = True

            truncated = False
            return np.array(next_state, dtype=np.float32), reward, truncated, done, {}

        except Exception as e:  # if there is an error, close the simulation
            print("An error occurred. Closing simulation.")
            print("Error: ", e)
            traci.close()

    def render(self):
        pass

    def close(self):
        try:
            traci.close()
        except:
            pass

    def seed(self, seed=None):
        pass

    # SUMO FUNCTIONS
    def sumo_step(self):
        new_state = [0] * (1 + 1 + 2 * self.bus_num)
        personsWaitingTimeList = []
        traci.simulationStep()

        vehicles = traci.vehicle.getIDList()
        persons = traci.person.getIDList()

        # finds the average waiting time
        for i in range(0, len(persons)):
            personWaitingTime = traci.person.getWaitingTime(persons[i])
            personsWaitingTimeList.append(personWaitingTime)

        persons_waiting_num = len(personsWaitingTimeList)

        if (persons_waiting_num != 0) and not np.isnan(persons_waiting_num) and not np.isnan(personsWaitingTimeList).any():
            new_state[0] = round(
                sum(personsWaitingTimeList) / persons_waiting_num, 3)
        else:
            new_state[0] = 0.0

        # find average people at bus stops
        new_state[1] = self.get_average_people_at_busstops()

        # finds bus speed and position
        bus_route_counter = [0, self.bus_num]
        for j in range(0, len(vehicles)):
            vehicleId = vehicles[j]
            vehicleSpeed_km_h = traci.vehicle.getSpeed(
                vehicleId)*3.6  # m/s to km/h
            vehicleRoute_index = 0 if (
                traci.vehicle.getRouteID(vehicleId) == "r_0") else 1
            vehiclePosition = traci.vehicle.getDistance(
                vehicleId) % (self.route_lengths[vehicleRoute_index])
            index_buffer = bus_route_counter[vehicleRoute_index]
            new_state[2 + index_buffer] = round(vehicleSpeed_km_h, 2)
            new_state[3 + index_buffer] = round(vehiclePosition, 2)
            bus_route_counter[vehicleRoute_index] += 2

        return new_state

    def _find_nearest(self, array, value):
        idx = np.searchsorted(array, value, side="left")
        if (idx == len(array) and math.fabs(value - (array[0] + array[idx-1])) < math.fabs(value - array[idx-1])):
            return array[0]
        elif idx > 0 and idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx]):
            return array[idx-1]
        else:
            return array[idx]

    def get_average_people_at_busstops(self):
        busstops = traci.busstop.getIDList()
        people_at_busstops = []
        for busstop in busstops:
            people_at_busstops.append(traci.busstop.getPersonCount(busstop))

        if len(people_at_busstops) == 0:
            return 0

        if sum(people_at_busstops) == 0:
            return 0

        return sum(people_at_busstops) / len(people_at_busstops)


gym.envs.registration.register(
    id='SumoEnv-v1',
    entry_point=SumoEnv,
    max_episode_steps=MAX_STEPS,
    reward_threshold=REWARD_THRESHOLD,
)
