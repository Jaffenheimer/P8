import numpy as np
from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironmentLearning import SumoEnv
from Constants import TOTAL_TIMESTEPS, N_ENVS
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")


def make_env():
    env = SumoEnv()
    return env


def run(modelType, name, policy):
    print(f"====================== <{name} Init> ======================")

    # Multi core
    env = SubprocVecEnv([make_env for _ in range(N_ENVS)])

    # Single core / Multi Threads
    # env = DummyVecEnv([make_env for _ in range(N_ENVS)])

    model_params = {"policy": policy, "env": env,
                    "verbose": 0, "device": "cpu"}

    model = modelType(**model_params)

    print(f"====================== <{name} Training> ======================")

    # # Train the agent
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True)

    # # Save the agent
    model.save(f"./Simulation/MachineLearning/Output/{name}")
 

if __name__ == "__main__":
    data = run(A2C, "A2C_both", "MlpPolicy")
    # data = run(PPO, "PPO", "MlpPolicy")
    # data = run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")
    # data = run(TRPO, "TRPO", "MlpPolicy")
