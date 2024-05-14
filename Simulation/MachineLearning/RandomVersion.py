import pandas as pd
from SumoEnvironment import SumoEnv
from random import randint
import numpy as np
from Constants import RANDOM_MAX_STEPS
from stable_baselines3.common.env_util import make_vec_env
from Helper.PlotDiagram import PlotBoth
from Helper.TOCSV import TOCSV


def RandomVersion():

    print("====================== <Random Init> ======================")

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1)

    obs = env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(RANDOM_MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    while not done:
        action = np.random.uniform(-1, 1, (1, 10)).astype('float32')
        # Perform a step in the environment
        obs, rewards, done, info = env.step(action)
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done:
            env.close()
            break

    # Save the data to a CSV file
    TOCSV(data, "Random")


    print("====================== <Random Done> ======================")

    return data[:-1]


def RandomMultiple(runs):
    for run in range(runs):
        print(f"====================== <RandomVersion Testing, run: {run}> ======================")

        env = make_vec_env(SumoEnv, n_envs=1)

        obs = env.reset()
        step = 0
        done = np.array([False], dtype='bool')

        while not done.all():
            action = np.random.uniform(-1, 1, (1, 10)).astype('float32')
            obs, rewards, done, info = env.step(action)

            data['AverageWaitTime'][step] = obs.item(0)
            data['AveragePeopleAtBusStops'][step] = obs.item(1)

            step += 1

            if done.all():
                env.close()
                break

    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs

    TOCSV(data, f"RandomMultipleRuns{runs}")

    return data[:-1]


if __name__ == "__main__":
    data = RandomVersion()
    data
    PlotBoth(data)
