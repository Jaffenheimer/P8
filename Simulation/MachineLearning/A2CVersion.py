from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from Helper.CSVWriter import CSVWriter
from SumoEnvironment import SumoEnv
from Helper.CollectionData import get_people_at_bus_stops
from stable_baselines3.common.vec_env import SubprocVecEnv
import numpy as np
from Constants import A2C_TOTAL_TIMESTEPS, A2C_MAX_STEPS
from Helper.PlotDiagram import PlotBoth


def A2CVersion():

    # Importing the environment
    env = make_vec_env(SumoEnv, n_envs=1, vec_env_cls=SubprocVecEnv)

    # Create the agent
    model = A2C("MlpPolicy", env, verbose=1)

    # Train the agent
    model.learn(total_timesteps=A2C_TOTAL_TIMESTEPS, progress_bar=True)

    # Save the agent
    # model.save("a2c_sumo")

    # del model  # remove to demonstrate saving and loading

    # # Load the trained agent
    # model = A2C.load("a2c_sumo")

    # Test the agent
    obs = env.reset()
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(A2C_MAX_STEPS, dtype=dtype)
    step = 0
    done = np.array([False], dtype='bool')

    while not done.all():
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        # print(f"Step: {step}, done: {done}")

        np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
        data['AverageWaitTime'][step] = obs.item(0)
        data['AveragePeopleAtBusStops'][step] = obs.item(1)
        step += 1

        if done.all():
            env.close()

    return data[:-1]


# if __name__ == "__main__":
#     A2CVersion()
