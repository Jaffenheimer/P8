from os import mkdir, path
from random import randint
import numpy as np
import pandas as pd
from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from SumoEnvironment import SumoEnv
from Constants import TOTAL_TIMESTEPS, MAX_STEPS, N_ENVS
from Helper.PlotDiagram import PlotBoth
from Helper.TOCSV import TOCSV
import gymnasium as gym

def make_env(env_id: str, rank: int, seed: int = 0):
    def _init(): 
        env = gym.make(env_id)
        env.reset()
        return env
    return _init
    


def run(modelType,name,policy):
    print(f"====================== <{name} Init> ======================")

    # Importing the environment
    #env = make_vec_env(SumoEnv, n_envs=N_ENVS)

    vec_env = SubprocVecEnv([make_env('SumoEnv-v1', i) for i in range(20)])

    #alternatively we could add such that you can pass the arguments to this function directly into the run function (as a dictionary) like this
    model_params = {"policy": policy, "env": vec_env, "verbose": 0, "n_steps": MAX_STEPS}
    if modelType != A2C:
        model_params["batch_size"] = 80
    
    # Create the agent
    model = modelType(**model_params)

    print(f"====================== <{name} Training> ======================")

    # Train the agent
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True)

    # Save the agent
    model.save(f"./Simulation/MachineLearning/Output/{name}")

    # del model  # remove to demonstrate saving and loading

    # Load the trained agent
    # model = modelType.load(f"{name}")

    print(f"====================== <{name} Traning Completed> ======================")

    # Test the agent
    obs = vec_env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():
        action, _ = model.predict(obs)

        obs, rewards, done, info = vec_env.step(action)
        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done.all():
            vec_env.close()

    # Save the data to a CSV file
    TOCSV(data, name)
    
    print(f"====================== <{name} Done> ======================")

    return data[:-1]

if __name__ == "__main__":
    data = run(PPO, "PPO", "MlpPolicy")
    data = run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")
    data = run(A2C, "A2C", "MlpPolicy")
    data = run(TRPO, "TRPO", "MlpPolicy")
    PlotBoth(data)