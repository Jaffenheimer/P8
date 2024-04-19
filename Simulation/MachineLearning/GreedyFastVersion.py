from Helper.PlotDiagram import PlotOneAveragePeopleAtBusstops, PlotBoth, PlotAverageWaitTime
from Helper.CollectionData import average_people_at_busstops
from stable_baselines3.common.env_util import make_vec_env
import numpy as np
from os import path, mkdir
from Constants import GREEDY_MAX_LEARN_STEPS
import gymnasium as gym


def GreedyFastVersion():

    # Importing the environment
    # env = SumoEnv()
    env = gym.make("SumoEnv-v1")

    obs = env.reset()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(GREEDY_MAX_LEARN_STEPS, dtype=dtype)

    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():

        action = np.array([1]*10, dtype='float32')

        # Perform a step in the environment
        obs, reward, truncated, done, _ = env.step(action)

        done = np.array([done], dtype='bool')

        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)

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
    PlotBoth(data[:-1])

    return data[:-1]


GreedyFastVersion()
