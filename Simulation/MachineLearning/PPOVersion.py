import numpy as np
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from SumoEnviroment import SumoEnv
from Helper.CollectionData import average_people_at_busstops
import asyncio
import warnings

warnings.filterwarnings('ignore', message='Person')  
def PPOVersion(timesteps=10000, steps=1000):
    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1)

    # Create the agent
    model = PPO("MlpPolicy", env, verbose=1)

    # Train the agent
    model.learn(total_timesteps=timesteps, progress_bar=True)

    # Save the agent
    model.save("ppo_sumo")

    del model  # remove to demonstrate saving and loading

    # Load the trained agent
    model = PPO.load("ppo_sumo")

    # Test the agent
    obs = env.reset()
    dtype = [ ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)
    step = 0

    while step < steps:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = obs.item(0)
        step += 1

    return data

