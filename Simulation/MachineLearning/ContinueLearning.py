import numpy as np
from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from SumoEnvironmentLearning import SumoEnv
from Constants import TOTAL_TIMESTEPS, N_ENVS
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from Constants import N_ENVS

def make_env():
    env = SumoEnv()
    return env


def run(modelType, modelNameToLoad, modelNameToSave):
    print(f"====================== <{modelNameToSave} Init> ======================")

    # Multi core
    env = SubprocVecEnv([make_env for _ in range(N_ENVS)])

    # Single core / Multi Threads
    # env = DummyVecEnv([make_env for _ in range(N_ENVS)])


    env = make_vec_env(SumoEnv, n_envs=N_ENVS)

    model_params = {"env": env,
                    "verbose": 0, "device": "cpu"}


    model = modelType.load(f"./Simulation/MachineLearning/Models/{modelNameToLoad}", **model_params)


    print(f"====================== <{modelNameToSave} Training> ======================")
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True, reset_num_timesteps=True)

    # Save the agent
    model.save(f"./Simulation/MachineLearning/Output/{modelNameToSave}LowHigh123123")


if __name__ == "__main__":
    data = run(A2C, "A2C_Low","A2C_Both")
    # data = run(PPO, "PPO_Low","PPO_Both")
    # data = run(RecurrentPPO, "RecurrentPPO_Low","RecurrentPPO_Both")
    # data = run(TRPO, "TRPO_Low","TRPO_Both")
