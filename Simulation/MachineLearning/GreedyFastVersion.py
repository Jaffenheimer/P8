import numpy as np
from os import path, mkdir
from Constants import GREEDY_MAX_STEPS
from SumoEnvironment import SumoEnv


def GreedyFastVersion():

    # Importing the environment
    env = SumoEnv()

    obs = env.reset()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(GREEDY_MAX_STEPS, dtype=dtype)

    obs = env.reset()
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
    return data[:-1]

if __name__ == "__main__":
    GreedyFastVersion()