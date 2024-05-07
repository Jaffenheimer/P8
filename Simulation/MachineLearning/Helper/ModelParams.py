from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from Constants import TUNING_STEPS


''' Functions for combined tunning of hyperparameters of different model (PPO, A2C, TRPO, etc.)'''
def get_model_params(trial):

    tunning_params = {
        "policy": None,
        "env": None,
        "verbose": 0,
        "device": 'auto',
        "n_steps": trial.suggest_int("n_steps", 10, 500, log=True),
    }


    return tunning_params
