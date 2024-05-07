from os import mkdir, path
from random import randint
import numpy as np
import pandas as pd
from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
from Constants import TOTAL_TIMESTEPS, MAX_STEPS, N_ENVS, UPDATEPOLICY
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from Helper.PlotDiagram import PlotBoth, PlotAverageWaitTime
from Helper.TOCSV import TOCSV
from Helper.FindAverage import FindAverage1

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")


def make_env():
    env = SumoEnv()
    return env


def run(modelType, name, policy):
    print(f"====================== <{name} Init> ======================")

    # Importing the environment
    env = make_vec_env(SumoEnv)

    # Load the trained agent
    # model = A2C.load("./Simulation/MachineLearning/PPO.zip")
    model = modelType.load(f"./Simulation/MachineLearning/Output/{name}")

    print(
        f"====================== <{name} Traning Completed> ======================")

    # Test the agent
    obs = env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    episode_starts = np.ones((N_ENVS,), dtype=bool)
    lstm_states = None

    while not done.all():
        if modelType == RecurrentPPO:
            action, lstm_states = model.predict(
                obs, state=lstm_states, episode_start=episode_starts)

        else:
            action, _ = model.predict(obs)

        obs, rewards, done, info = env.step(action)

        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)

        episode_starts = done

        step += 1

        if done.all():
            env.close()

    # Save the data to a CSV file
    TOCSV(data, name, "Combined")

    print(f"====================== <{name} Done> ======================")

    return data[:-1]


if __name__ == "__main__":
    data = run(PPO, "PPO", "MlpPolicy")
    # data = run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")
    # data = run(A2C, "A2C", "MlpPolicy")
    # data = run(TRPO, "TRPO", "MlpPolicy")
    # PlotBoth(data)
    FindAverage1(data)
    PlotAverageWaitTime(data)
