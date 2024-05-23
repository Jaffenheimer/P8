import numpy as np
from tqdm import tqdm
from Constants import GREEDY_MAX_STEPS, MAX_STEPS
from Simulation.MachineLearning.SumoEnvironmentTesting import SumoEnv
from stable_baselines3.common.env_util import make_vec_env
from Helper.TOCSV import TOCSV

def GreedyFastVersion():

    print("====================== <Greedy Fast Init> ======================")

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1)

    obs = env.reset()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(GREEDY_MAX_STEPS, dtype=dtype)

    obs = env.reset()
    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():
        action = np.ones((1, 10), dtype='float32')
        # Perform a step in the environment
        obs, rewards, done, info = env.step(action)
        done = np.array([done], dtype='bool')
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)

        step += 1

        if done.all():
            env.close()
            
    # Save the data to a CSV file
    TOCSV(data, "GreedyFast")

    print("====================== <Greedy Fast Done> ======================")

    return data[:-1]

def GreedyMultiple(runs): 
    for run in range(runs):
        print(f"====================== <GreedyFastVersion Testing, run: {run}> ======================")

        env = make_vec_env(SumoEnv, n_envs=1)

        obs = env.reset()
        step = 0
        done = np.array([False], dtype='bool')

        with tqdm(total=MAX_STEPS, desc="Greedy Progress") as pbar:
            while not done.all():
                action = np.ones((1, 10), dtype='float32')
                obs, rewards, done, info = env.step(action)
                data['AverageWaitTime'][step] += obs.item(0)
                data['AveragePeopleAtBusStops'][step] += obs.item(1)
                step += 1
                pbar.update(1)

                if step==MAX_STEPS-1:
                    pbar.update(1)
                    pbar.close()
                    
                if done.all():
                    env.close()

    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs

    TOCSV(data, f"GreedyFastMultipleRuns{runs}")

    return data[:-1]


if __name__ == "__main__":
    data = GreedyFastVersion()
    dataMul = GreedyMultiple(5)