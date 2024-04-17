from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from SumoEnviroment import SumoEnv
from Helper.CollectionData import avarage_people_at_busstops
import numpy as np
import asyncio


async def A2CVersion(time_steps=10000, steps=1000):
    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1)

    # Create the agent
    model = A2C("MlpPolicy", env, verbose=1)

    # Train the agent
    model.learn(total_timesteps=time_steps, progress_bar=True)

    # Save the agent
    model.save("a2c_sumo")

    del model  # remove to demonstrate saving and loading

    # Load the trained agent
    model = A2C.load("a2c_sumo")

    # Test the agent
    obs = env.reset()
    waiting_times_A2C = []  # List to store average waiting time at each step
    people_at_busstops = []
    step = 0

    while step < steps:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        waiting_times_A2C.append(obs.item(0))
        people_at_busstops.append(avarage_people_at_busstops())
        step += 1

    return waiting_times_A2C, people_at_busstops

asyncio.run(A2CVersion())  # Run the async function within an event loop
