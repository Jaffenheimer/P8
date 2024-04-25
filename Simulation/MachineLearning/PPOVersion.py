from random import randint
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
from Constants import PPO_TOTAL_TIMESTEPS, PPO_MAX_STEPS
from Helper.PlotDiagram import PlotBoth


def PPOVersion():

    print("====================== <PPO Init> ======================")

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=4)

    # Create the agent
    model = PPO("MlpPolicy", env, verbose=1,
                n_steps=PPO_MAX_STEPS, batch_size=80)

    print("====================== <PPO Training> ======================")

    # Train the agent
    model.learn(total_timesteps=PPO_TOTAL_TIMESTEPS, progress_bar=True)

    # Save the agent
    # model.save("ppo_sumo")

    # del model  # remove to demonstrate saving and loading

    # Load the trained agent
    # model = PPO.load("ppo_sumo")

    print("====================== <PPO Traning Completed> ======================")

    # Test the agent
    obs = env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(PPO_MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():
        action, _ = model.predict(obs)

        obs, rewards, done, info = env.step(action)
        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done.all():
            env.close()

    print("====================== <PPO Done> ======================")
    return data[:-1]


if __name__ == "__main__":
    data = PPOVersion()
    PlotBoth(data)
