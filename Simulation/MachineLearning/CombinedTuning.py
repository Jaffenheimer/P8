from os import mkdir, path
import optuna
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from sb3_contrib import TRPO, RecurrentPPO
from optuna.samplers import TPESampler
import numpy as np
from Constants import TUNING_STEPS, TUNING_TOTAL_TIMESTEPS, TUNING_TRIALS
from SumoEnvironment import SumoEnv

''' Functions for combined tunning of hyperparameters of different model (PPO, A2C, TRPO, etc.)'''


def Objective(trial: optuna.Trial, modelType, policy):
    # Define hyperameters to tune

    n_envs = trial.suggest_int("n_envs", 4, 8)
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)
    gamma = trial.suggest_float("gamma", 0.9, 0.999, log=True)
    gae_lambda = trial.suggest_float("gae_lambda", 0.8, 0.99, log=True)

    if modelType != A2C or modelType != TRPO:
        batch_size = trial.suggest_int("batch_size", 64, 128, log=True)
        ent_coef = trial.suggest_float("ent_coef", 0.00000001, 0.1, log=True)
        vf_coef = trial.suggest_float("vf_coef", 0.00000001, 0.5, log=True)

        # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=n_envs)

    model_params = {"policy": policy, "env": env, "verbose": 0, "learning_rate": learning_rate,
                    "gamma": gamma, "gae_lambda": gae_lambda, "device": 'auto', "n_steps": TUNING_STEPS}

    if modelType != A2C or modelType != TRPO:
        model_params["ent_coef"] = ent_coef
        model_params["vf_coef"] = vf_coef
        model_params["batch_size"] = batch_size

    # Create the model with the hyperparameters
    model = modelType(**model_params)

    # Train the model
    model.learn(total_timesteps=TUNING_TOTAL_TIMESTEPS)

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
        trial, modelType, policy), n_trials=TUNING_TRIALS)

    best_trial = study.best_trial.params
    print(f"Best trial: {best_trial}")

    if not path.isdir("./Simulation/MachineLearning/Output"):
        mkdir("./Simulation/MachineLearning/Output")
    with open(f"./Simulation/MachineLearning/Output/best_trial_{name}.csv", "w") as f:
        f.write(str(best_trial))


if __name__ == "__main__":
    CombinedTuning(PPO, "MlpPolicy", "PPO")
    # CombinedTuning(A2C, "MlpPolicy", "A2C")
    # CombinedTuning(TRPO, "MlpPolicy", "TRPO")
    # CombinedTuning(RecurrentPPO, "MlpLstmPolicy", "RecurrentPPO")
