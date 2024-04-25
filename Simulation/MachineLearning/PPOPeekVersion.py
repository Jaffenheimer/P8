from random import randint
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
from Constants import PPO_TOTAL_TIMESTEPS, PPO_MAX_STEPS, PEEK_LEARN_STEPS, PEEK_INTERVAL

def PPOPeekVersion():

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1)

    # Create the agent
    model = PPO("MlpPolicy", env, verbose=1, n_steps=PPO_MAX_STEPS)

    # Train the agent
    model.learn(total_timesteps=PPO_TOTAL_TIMESTEPS, progress_bar=True)

    # Save the agent
    # model.save("ppo_sumo")

    # del model  # remove to demonstrate saving and loading

    # Load the trained agent
    # model = PPO.load("ppo_sumo")

    # Test the agent
    obs = env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(PPO_MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')
    np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

    for step in range(PPO_MAX_STEPS):
        action, _ = model.predict(obs)
        obs, rewards, done, info = env.step(action)

        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done.all():
            env.close()
            break
        elif step % PEEK_INTERVAL == PEEK_INTERVAL:
            model.learn(PEEK_LEARN_STEPS)

    return data[:-1]