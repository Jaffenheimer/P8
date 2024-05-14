from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from sb3_contrib import RecurrentPPO, TRPO
from SumoEnvironment import SumoEnv
from Helper.TOCSV import RUNNING_TOCSV
from Constants import N_ENVS, MAX_STEPS

import numpy as np
from tqdm import tqdm

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

def Running(modelType, name, runs):
    
    env = make_vec_env(SumoEnv, n_envs=1)
    for run in range(runs): 
        
        print(f"====================== <{name} Running, run: {run}> ======================")
        
        model = modelType.load(f"./Simulation/MachineLearning/input/{name}")

        # Test the model
        obs = env.reset()
        step = 0
        done = np.array([False], dtype='bool')

        episode_starts = np.ones((1,), dtype=bool)
        lstm_states = None

        # Run the simulation until all the buses have reached their destination
        with tqdm(total=MAX_STEPS, desc="Testing Progress") as pbar:
            while not done.all():
                if modelType == RecurrentPPO:
                    action, lstm_states = model.predict(
                    obs, state=lstm_states, episode_start=episode_starts)
                else:
                    action, _ = model.predict(obs)

                obs, rewards, done, info = env.step(action)
                if done.all():
                    env.close()
                    break

                if step % 5 == 0:
                    RUNNING_TOCSV(obs)

                episode_starts = done

                step += 1
                pbar.update(1)

                if step==MAX_STEPS-1:
                    pbar.update(1)
                    pbar.close()

            del model
            lstm_states = None
            episode_starts = np.ones((1,), dtype=bool)
    return

if __name__ == "__main__":
    Running(PPO, "PPO_low", 1)
