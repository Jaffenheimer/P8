import pandas as pd
from SumoEnvironment import SumoEnv
from random import randint
import numpy as np
from Constants import RANDOM_MAX_STEPS
from Helper.PlotDiagram import PlotBoth
from Helper.TOCSV import TOCSV


def RandomVersion():

    print("====================== <Random Init> ======================")

    # Importing the environment
    env = SumoEnv()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(RANDOM_MAX_STEPS, dtype=dtype)

    step = 0
    obs = env.reset()

    done = np.array([False], dtype='bool')

    while not done:
        action = [randint(-1, 1) for i in range(10)]

        # Perform a step in the environment
        obs, reward, truncated, done, _ = env.step(action)
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done:
            env.close()

    # Save the data to a CSV file
    TOCSV(data, "Random")


    print("====================== <Random Done> ======================")

    return data[:-1]


if __name__ == "__main__":
    data = RandomVersion()
    PlotBoth(data)
