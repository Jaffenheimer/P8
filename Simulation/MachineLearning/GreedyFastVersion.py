from Helper.PlotDiagram import PlotOneAveragePeopleAtBusstops, PlotBoth, PlotAverageWaitTime
from Helper.CollectionData import average_people_at_busstops
from stable_baselines3.common.env_util import make_vec_env
from SumoEnviroment import SumoEnv
import numpy as np
from os import path, mkdir
from Constants import GREEDY_MAX_LEARN_STEPS


def GreedyFastVersion():

    # Importing the environment
    env = SumoEnv()

    obs = env.reset()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(GREEDY_MAX_LEARN_STEPS, dtype=dtype)

    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():

        action = np.array([1]*10, dtype='float32')

        # Perform a step in the environment
        obs, reward, done, info, truncated = env.step(action)
        done = np.array([done], dtype='bool')

        print(
            f"Step: {step}, done: {done}, donetype: {type(done)}, env: {env.current_step}, env_max: {env.max_steps}, actions{action}")
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = obs.item(0)

        step += 1

        if done.all():
            env.close()

    # Save the data to a CSV file
    if (path.isdir("../Output") == False):
        mkdir("../Output")
    np.savetxt(f"../Output/GreedyFastVersion.csv", data, delimiter=',',
               fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime")

    # PlotAverageWaitTime(waiting_times_greedy_fast)
    # PlotOneAveragePeopleAtBusstops(people_at_busstops)
    PlotBoth(data)

    return data


GreedyFastVersion()
