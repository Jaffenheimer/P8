from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from Constants import TUNING_STEPS


''' Functions for combined tunning of hyperparameters of different model (PPO, A2C, TRPO, etc.)'''
def get_model_params(modelType, trial):

    n_envs = trial.suggest_int("n_envs", 4, 8)  # Number of environments

    base_params = {
        "policy": None,
        "env": None,
        "verbose": 0,
        "gamma": trial.suggest_float("gamma", 0.9, 0.999, log=True),
        "gae_lambda": trial.suggest_float("gae_lambda", 0.8, 0.99, log=True),
        "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True),
        "device": 'auto',
        "n_steps": TUNING_STEPS,
        "gamma": trial.suggest_float("gamma", 0.9, 0.999, log=True),
        "gae_lambda": trial.suggest_float("gae_lambda", 0.8, 0.99, log=True),
    }

    if modelType == A2C:
        a2c_params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True),
            # "gamma": trial.suggest_float("gamma", 0.9, 0.999, log=True),
            # "gae_lambda": trial.suggest_float("gae_lambda", 0.8, 0.99, log=True),
            "ent_coef": trial.suggest_float("ent_coef", 0.00000001, 0.1, log=True),
            "vf_coef": trial.suggest_float("vf_coef", 0.00000001, 0.5, log=True),
            "max_grad_norm": trial.suggest_float("max_grad_norm", 0.3, 1.0, log=True)
        }
        base_params.update(a2c_params)
    elif modelType == PPO:
        ppo_params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True),
            "batch_size": trial.suggest_int("batch_size", 64, 128, log=True),
            "clip_range": trial.suggest_float("clip_range", 0.1, 0.4),
            "ent_coef": trial.suggest_float("ent_coef", 0.00000001, 0.1, log=True),
            "vf_coef": trial.suggest_float("vf_coef", 0.00000001, 0.5, log=True),
            "max_grad_norm": trial.suggest_float("max_grad_norm", 0.3, 1.0, log=True),
        }
        base_params.update(ppo_params)
    elif modelType == TRPO:
        trpo_params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True),
            "batch_size": trial.suggest_int("batch_size", 64, 128, log=True),
            "target_kl": trial.suggest_float("target_kl", 0.01, 0.1),
            "cg_max_steps": trial.suggest_int("cg_max_steps", 10, 20),
            "cg_damping": trial.suggest_float("cg_damping", 0.1, 0.3),
            "line_search_shrinking_factor": trial.suggest_float("line_search_shrinking_factor", 0.1, 0.3),
            "line_search_max_iter": trial.suggest_int("line_search_max_iter", 10, 20),
            "n_critic_updates": trial.suggest_int("n_criitc_updates", 1, 10)
        }
        base_params.update(trpo_params)
    elif modelType == RecurrentPPO:
        recurrent_ppo_params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True),
            "batch_size": trial.suggest_int("batch_size", 64, 128, log=True),
            "clip_range": trial.suggest_float("clip_range", 0.1, 0.4),
            "ent_coef": trial.suggest_float("ent_coef", 0.00000001, 0.1, log=True),
            "vf_coef": trial.suggest_float("vf_coef", 0.00000001, 0.5, log=True),
            "max_grad_norm": trial.suggest_float("max_grad_norm", 0.3, 1.0, log=True)
        }
        base_params.update(recurrent_ppo_params)

    return base_params, n_envs
