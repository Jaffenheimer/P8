import json
import optuna
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from optuna.samplers import TPESampler
from SumoEnvironment import SumoEnv
import numpy as np

'''  This script is used to tune the hyperparameters of the PPO algorithm using Optuna.'''

# Define a function to optimize


def objective(trial: optuna.Trial):
    # Define hyperameters to tune
    n_envs = trial.suggest_int("n_envs", 4, 8)
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)
    ent_coef = trial.suggest_float("ent_coef", 0.00000001, 0.1, log=True)
    vf_coef = trial.suggest_float("vf_coef", 0.00000001, 0.5, log=True)
    gamma = trial.suggest_float("gamma", 0.9, 0.999, log=True)
    gae_lambda = trial.suggest_float("gae_lambda", 0.8, 0.99, log=True)
    batch_size = trial.suggest_int("batch_size", 64, 128, log=True)

    # Print original hyperparameters
    print("Original Hyperparameters:")
    print(f"\tn_envs: {n_envs}")
    print(f"\tlearning_rate: {learning_rate}")
    print(f"\tent_coef: {ent_coef}")
    print(f"\tgamma: {gamma}")
    print(f"\tgae_lambda: {gae_lambda}")

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=n_envs)

    # Create the model with the hyperparameters
    model = PPO("MlpPolicy", env=env, verbose=0, learning_rate=learning_rate,
                ent_coef=ent_coef, vf_coef=vf_coef, gamma=gamma, gae_lambda=gae_lambda, batch_size=batch_size, device='auto', n_steps=1000)

    # Train the model
    model.learn(total_timesteps=10000)

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


# Optimize the hyperparameters using Optuna
study = optuna.create_study(direction="minimize")

study.optimize(objective, n_trials=10, show_progress_bar=True)

# Retrive the best hyperparameters
best_trial = study.best_trial

# Extract the best hyperparameters
# best_batch_size = best_trial.params["batch_size"]
# best_learning_rate = best_trial.params["learning_rate"]
# best_n_envs = best_trial.params["n_envs"]
# best_gamma = best_trial.params["gamma"]
# best_gae_lambda = best_trial.params["gae_lambda"]
# best_ent_coef = best_trial.params["ent_coef"]
# best_vf_coef = best_trial.params["vf_coef"]

# Print the best hyperparameters
print("Best trail: ", best_trial.params)

# Write the best hyperparameters to a CSV file
with open("best_hyperparameters.csv", "w") as f:
    json.dump(best_trial.params, f)
