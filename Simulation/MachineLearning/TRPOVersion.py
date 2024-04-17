from sb3_contrib import TRPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnviroment import SumoEnv
from Helper.CollectionData import average_people_at_busstops
import asyncio
import numpy as np


def TRPOVersion(timesteps=10000, steps=1000):
    env = make_vec_env(SumoEnv, n_envs=1)

    model = TRPO("MlpPolicy", env, verbose=1)

    model.learn(total_timesteps=timesteps,
                tb_log_name="TRPO_SUMO", progress_bar=True)

    model.save("trpo_sumo")

    del model

    model = TRPO.load("trpo_sumo")
    obs = env.reset()
    step = 0
    dtype = [ ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)


    while step < steps:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = obs.item(0)

        step += 1

    return data
