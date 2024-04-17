from sb3_contrib import TRPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnviroment import SumoEnv
from Helper.CollectionData import avarage_people_at_busstops
import asyncio


async def TRPOVersion(timesteps=10000, steps=1000):
    env = make_vec_env(SumoEnv, n_envs=1)

    model = TRPO("MlpPolicy", env, verbose=1)

    model.learn(total_timesteps=timesteps,
                tb_log_name="TRPO_SUMO", progress_bar=True)

    model.save("trpo_sumo")

    del model

    model = TRPO.load("trpo_sumo")
    obs = env.reset()
    step = 0
    waiting_times_TRPO = []
    people_at_busstops = []

    while step < steps:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        people_at_busstops.append(avarage_people_at_busstops())
        waiting_times_TRPO.append(obs.item(0))

        step += 1

    return waiting_times_TRPO, people_at_busstops

asyncio.run(TRPOVersion())
