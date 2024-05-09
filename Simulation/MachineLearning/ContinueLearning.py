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

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")


def make_env():
    env = SumoEnv()
    return env


def run(modelType, name, policy):
    print(f"====================== <{name} Init> ======================")

    # Importing the environment
    # env = make_vec_env(SumoEnv, n_envs=N_ENVS)

    # Multi core
    env = SubprocVecEnv([make_env for _ in range(N_ENVS)])

    # Single core / Multi Threads
    # env = DummyVecEnv([make_env for _ in range(N_ENVS)])

    # #alternatively we could add such that you can pass the arguments to this function directly into the run function (as a dictionary) like this
    model_params = {"policy": policy, "env": env,
                    "verbose": 0, "n_steps": UPDATEPOLICY}
    # if modelType != A2C:
    #     model_params["batch_size"] = 80


    print(f"====================== <{name} Loading> ======================")
    model = modelType.load(f"./Simulation/MachineLearning/Output/{name}", **model_params)

    #model.set_env(env)
    print(f"====================== <{name} Training> ======================")

    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True)


    # Save the agent
    model.save(f"./Simulation/MachineLearning/Output/{name}LowHigh")


if __name__ == "__main__":
    data = run(PPO, "PPO", "MlpPolicy")
    # data = run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")
    # data = run(A2C, "A2C", "MlpPolicy")
    # data = run(TRPO, "TRPO", "MlpPolicy")
    # PlotBoth(data, "PPO")
