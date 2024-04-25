from random import randint
from sb3_contrib import TRPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
from Helper.CollectionData import average_people_at_busstops
import numpy as np
from Constants import TRPO_TOTAL_TIMESTEPS, TRPO_MAX_STEPS


def TRPOVersion():

    env = make_vec_env(SumoEnv, n_envs=1)

    model = TRPO(policy="MlpPolicy", env=env, verbose=1, n_steps=TRPO_MAX_STEPS)

    model.learn(total_timesteps=TRPO_TOTAL_TIMESTEPS,
                tb_log_name="TRPO_SUMO", progress_bar=True)

    # model.save("trpo_sumo")

    # del model

    # model = TRPO.load("trpo_sumo")
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(TRPO_MAX_STEPS, dtype=dtype)

    obs = env.reset()
    step = 0

    done = np.array([False], dtype='bool')

    while not done.all():
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)

        step += 1

        if done.all():
            env.close()

    return data[:-1]

if __name__ == "__main__":
    TRPOVersion()
