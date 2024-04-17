import os
import gymnasium as gym
import numpy as np
import traci
import math
from os import path


class SumoEnv(gym.Env):
    def __init__(self):
        self.close()  # tries to close, if not possible, pass

        traci.start(
            ["sumo", "-c", path.abspath("../SUMO/algorithm/algorithm.sumocfg")])

        ## VARIABLES ##
        self.bus_num = 5
        self.max_steps = 500
        self.current_step = 0
        bus_stops_num = 4
        bus_speed_max = 50

        ## SUMO VARIABLES ##
        self.bus_stop_positions = [
            [123, 974, 1872, 2764], [123, 827, 1742, 2702, 3592]]
        self.bus_locations = {"-overlap": "123", "-R2": "259", "-R1": "125",
                              "-R0": "267", "-L3": "117", "-L2": "110", "-L1": "123", "-L0": "120"}
        self.bus_ids = ["bus_r_0_0", "bus_r_0_1",
                        "bus_r_0_2", "bus_r_0_3", "bus_r_0_4"]

        # self.route_names = [["-overlap", "-R2", "-R1", "-R0"], ["-overlap", "-L3", "-L2", "-L1", "-L0"]]
        self.route_lengths = [3591, 4697]
        # self.route_junctions={"J1": ["-L0", "-R0", "-overlap"], "J2": ["-R0", "-R1"], "J3": ["-R1", "-R2"], "J4": ["-L3", "-R2", "-overlap"], "J5": ["-L0", "-L1"], "J7": ["-L1", "-L2"], "J8": ["-L2", "-L3"]}

        self.wait_time = 0
        self.previous_speeds_m_s = [0]*self.bus_num
        self.delta_speed = 0.4
        self.min_speed_before_change = 30
        self.action_delta_speed = {
            -1: (1-self.delta_speed), 1: (1+self.delta_speed)}

        ## GYM INITIALIZATIONS ##

        # actions: [b1, b2 (...)] # each action is either -1 = slow down, 0 = keep speed, 1 = speed up
        self.action_space = gym.spaces.Box(low=np.array(
            [np.float32(-1)]*self.bus_num), high=np.array([np.float32(1)]*self.bus_num), shape=(self.bus_num,), dtype=np.float32)

        # states: [avg_wait_time, b1_speed, b1_pos, b2_speed, b2_pos, (...),  bs1_pos, bs2_pos, bs3_pos, bs4_pos]
        wait_max = 100000
        low_obs = np.zeros([1 + 2*self.bus_num + bus_stops_num])
        high_obs = np.array([wait_max] + [bus_speed_max, self.route_lengths[0]]
                            * self.bus_num + [self.route_lengths[0]]*bus_stops_num)
        self.observation_space = gym.spaces.Box(low=low_obs, high=high_obs, shape=(
            1 + 2*self.bus_num + bus_stops_num,), dtype=np.float32)

    # GYM FUNCTIONS
    def reset(self, seed=None, options=None):
        traci.close()
        self.wait_time = 0
        self.current_step = 0
        traci.start(
            ["sumo", "-c", path.abspath("../SUMO/algorithm/algorithm.sumocfg")])

        # return self.wait_time, {}
        return np.concatenate(([self.wait_time], np.zeros(2 * self.bus_num), self.bus_stop_positions[0])).astype(np.float32)[:15], {}

    def step(self, action):
        # try:
        next_state = self.sumo_step()

        # set action for each bus: -1 = slow down, 0 = keep speed, 1 = speed up
        vehicles_length = len(traci.vehicle.getIDList())

        for i, bus_action in enumerate(action):
            if i >= vehicles_length:
                break
            bus_action = round(bus_action)
            bus_id = self.bus_ids[i]
            bus_distance_driven = traci.vehicle.getDistance(bus_id)

            if np.sign(bus_distance_driven) == -1:
                break  # if bus hasnt driven yet, skip

            bus_route = traci.vehicle.getRouteID(bus_id)
            bus_position = round(bus_distance_driven % (
                self.route_lengths[0] if (bus_route == "r_0") else self.route_lengths[1]), 3)
            nearest_bus_stop_position = self._find_nearest(
                self.bus_stop_positions[0 if bus_route == "r_0" else 1], bus_position)
            bus_speed_m_s = traci.vehicle.getSpeed(bus_id)
            bus_speed_km_t = bus_speed_m_s * 3.6

            interval = [-22, 3]

            new_speed_m_s = 0

            # if bus should keep speed, set speed to previous speed and if previous speed is 0, set to current speed
            if bus_action == 0:
                new_speed_m_s = bus_speed_m_s if (self.previous_speeds_m_s[i] == 0.0) \
                    else self.previous_speeds_m_s[i]
                traci.vehicle.setSpeed(bus_id, new_speed_m_s)

            # change speed if speed > min_speed_before_change and bus is not at a bus stop
            elif (bus_speed_km_t > self.min_speed_before_change and not
                  (bus_position > nearest_bus_stop_position + interval[0] and bus_position < nearest_bus_stop_position + interval[1])):
                new_speed_m_s = self.action_delta_speed[bus_action] * \
                    traci.vehicle.getSpeed(bus_id)
                # smoothly changes to new speed over 1 second
                traci.vehicle.slowDown(bus_id, new_speed_m_s, 1)

            self.previous_speeds_m_s[i] = new_speed_m_s

        # reward are given if the new waiting time is strictly lower, otherwise punished
        reward = 1 if next_state[0] <= self.wait_time else -1

        # set the wait time to the current wait time
        self.wait_time = next_state[0]

        # check if done
        self.current_step += 1
        done = False
        if (self.current_step >= self.max_steps):
            done = True

        truncated = False
        return np.array(next_state, dtype=np.float32), reward, truncated, done, {}

        # except Exception as e:  # if there is an error, close the simulation
        #   print("An error occurred. Closing simulation.")
        #   print("Error: ", e)
        #   traci.close()

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
        # state [avg_wait_time, b1_speed, b1_pos, b2_speed, b2_pos, (...),  bs1_pos, bs2_pos, bs3_pos, bs4_pos]
        new_state = [0] * (1 + 2 * self.bus_num) + self.bus_stop_positions[0]
        personsWaitingTimeList = []
        traci.simulationStep()

        vehicles = traci.vehicle.getIDList()
        persons = traci.person.getIDList()

        # finds the average waiting time
        for i in range(0, len(persons)):
            personWaitingTime = traci.person.getWaitingTime(persons[i])
            personsWaitingTimeList.append(personWaitingTime)

        persons_waiting_num = len(personsWaitingTimeList)
        new_state[0] = round(sum(personsWaitingTimeList) / persons_waiting_num, 3) if persons_waiting_num > 0 or not np.isnan(
            persons_waiting_num) or not np.isnan(personsWaitingTimeList) else 0.0

        # finds bus speed and position
        for j in range(0, len(vehicles)):
            vehicleId = vehicles[j]
            if traci.vehicle.getRouteID(vehicleId) != "r_0":
                continue

            vehicleSpeed = traci.vehicle.getSpeed(vehicleId)*3.6  # m/s to km/h
            vehiclePosition = traci.vehicle.getDistance(vehicleId) % (self.route_lengths[0]
                                                                      if (traci.vehicle.getRouteID(vehicleId) == "r_0") else self.route_lengths[1])
            new_state[1 + 2*j] = round(vehicleSpeed, 2)
            new_state[2 + 2*j] = round(vehiclePosition, 2)
        return new_state

    def _find_nearest(self, array, value):
        idx = np.searchsorted(array, value, side="left")
        if (idx == len(array) and math.fabs(value - (array[0] + array[idx-1])) < math.fabs(value - array[idx-1])):
            return array[0]
        elif idx > 0 and idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx]):
            return array[idx-1]
        else:
            return array[idx]


''' PPO SUMO TRAINING '''
logdir = "logs"

if not os.path.exists(logdir):
    os.makedirs(logdir)


# Register the environment
gym.register(
    "SumoEnv-v0",
    entry_point=SumoEnv,
    max_episode_steps=500,
    reward_threshold=1000,
)
