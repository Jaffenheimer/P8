from os import mkdir, path
import optuna
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from sb3_contrib import TRPO, RecurrentPPO
from optuna.samplers import TPESampler
import numpy as np
from Helper.ModelParams import get_model_params
from Constants import TUNING_TOTAL_TIMESTEPS, TUNING_TRIALS, N_ENVS
from stable_baselines3.common.vec_env import SubprocVecEnv
from SumoEnvironment import SumoEnv


def make_env():
    env = SumoEnv()
    return env

def Objective(trial: optuna.Trial, modelType, policy):  
    
    #model_params, n_envs = get_model_params(modelType, trial)
    model_params = get_model_params(trial=trial)
    
    model_params["policy"] = policy

    # Muli core
    env = SubprocVecEnv([make_env for _ in range(N_ENVS)])

    model_params["env"] = env

    model = modelType(**model_params)

    # Train the model
    model.learn(total_timesteps=TUNING_TOTAL_TIMESTEPS, progress_bar=True)

    # Evaluate the model
    obs = env.reset()
    rewards = 0
    done = np.array([False], dtype='bool')

    while not done.all():
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        rewards += np.mean(reward)

        if done.all():
            env.close()

    return -rewards


def CombinedTuning(modelType, policy, name):
    study = optuna.create_study(direction="minimize", sampler=TPESampler())
    study.optimize(lambda trial: Objective(
        trial, modelType, policy), n_trials=TUNING_TRIALS, show_progress_bar=True)

    best_trial = study.best_trial.params

    if not path.isdir("./Simulation/MachineLearning/Output/TuningFiles"):
        mkdir("./Simulation/MachineLearning/Output/TuningFiles")
    with open(f"./Simulation/MachineLearning/Output/TuningFiles/best_trial_{name}.csv", "w") as f:
        f.write(
            f"Best trial for {name} (Trials: {TUNING_TRIALS}, Total Timesteps: {TUNING_TOTAL_TIMESTEPS}:\n")
        for key, value in best_trial.items():
            f.write(f"{key}: {value}\n")


if __name__ == "__main__":
    # CombinedTuning(PPO, "MlpPolicy", "PPO")
    CombinedTuning(A2C, "MlpPolicy", "A2C")
    # CombinedTuning(TRPO, "MlpPolicy", "TRPO")
    # CombinedTuning(RecurrentPPO, "MlpLstmPolicy", "RecurrentPPO")
