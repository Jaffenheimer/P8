from random import randint
import numpy as np
from stable_baselines3 import A2C, PPO
from sb3_contrib import TRPO, RecurrentPPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
from stable_baselines3.common.vec_env import SubprocVecEnv
from Constants import TOTAL_TIMESTEPS, MAX_STEPS, N_ENVS, PEEK_INTERVAL, PEEK_LEARN_STEPS
from Helper.PlotDiagram import PlotBoth
import gymnasium as gym


def run(modelType,name,policy):
    print(f"====================== <{name} Init> ======================")

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=N_ENVS)

    #alternatively we could add such that you can pass the arguments to this function directly into the run function (as a dictionary) like this
    model_params = {"policy": policy, "env": env,
                    "verbose": 0, "n_steps": MAX_STEPS}
    if modelType != A2C:
        model_params["batch_size"] = 80
    
    # Create the agent
    model = modelType(**model_params)

    print(f"====================== <{name} Training> ======================")

    # Train the agent
    model.learn(total_timesteps=TOTAL_TIMESTEPS, progress_bar=True)

    # Save the agent
    # model.save(f"./Simulation/MachineLearning/Output/{name}Peek")


    # del model  # remove to demonstrate saving and loading

    # Load the trained agent
    # model = modelType.load(f"{name}")

    print(f"====================== <{name} Traning Completed> ======================")

    # Test the agent
    obs = vec_env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    for _ in range(MAX_STEPS):
        action, _ = model.predict(obs)

        obs, rewards, done, info = env.step(action)
        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done.all():
            env.close()
            break
        elif step % PEEK_INTERVAL == PEEK_INTERVAL:
            model.learn(PEEK_LEARN_STEPS)

    print(f"====================== <{name} Done> ======================")
    return data[:-1]

if __name__ == "__main__":
    data = run(PPO, "PPO", "MlpPolicy")
    data = run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")
    data = run(A2C, "A2C", "MlpPolicy")
    data = run(TRPO, "TRPO", "MlpPolicy")
    PlotBoth(data)