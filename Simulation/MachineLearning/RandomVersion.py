import pandas as pd
from SumoEnvironment import SumoEnv
from random import randint
import numpy as np
from Constants import RANDOM_MAX_STEPS
from stable_baselines3.common.env_util import make_vec_env
from Helper.PlotDiagram import PlotAverageWaitTimeMultiple
from Helper.TOCSV import TOCSV
from Helper.FindAverage import findAverageWaitTime
from tqdm import tqdm


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
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(RANDOM_MAX_STEPS, dtype=dtype)
    env = make_vec_env(SumoEnv, n_envs=1)
    
    for run in range(runs):
        print(f"====================== <RandomVersion Testing, run: {run}> ======================")

        obs = env.reset()
        step = 0
        done = np.array([False], dtype='bool')


        with tqdm(total=RANDOM_MAX_STEPS, desc="Testing Progress") as pbar:
            while not done.all():
                action = np.random.uniform(-1, 1, (1, 10)).astype('float32')
                obs, rewards, done, info = env.step(action)

                data['AverageWaitTime'][step] += obs.item(0)
                data['AveragePeopleAtBusStops'][step] += obs.item(1)

                step += 1
                pbar.update(1)

                if step==RANDOM_MAX_STEPS-1:
                    pbar.update(1)
                    pbar.close()

                if done.all():
                    env.close()
                    


    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs

    TOCSV(data, f"RandomMultipleRuns{runs}")

    return data[:-1]


if __name__ == "__main__":
    # data = RandomVersion()
    dataMiltiple = RandomMultiple(5)
    print(f"Average wait time: {np.average(dataMiltiple['AverageWaitTime']):.2f}\n")
    findAverageWaitTime(("Random", dataMiltiple))
    PlotAverageWaitTimeMultiple(("Random", dataMiltiple))
