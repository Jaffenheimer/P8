from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from sb3_contrib import RecurrentPPO, TRPO
from SumoEnvironment import SumoEnv
from Helper.TOCSV import TOCSV
from Constants import N_ENVS, MAX_STEPS
from Helper.PlotDiagram import PlotAverageWaitTimeMultiple

import numpy as np
from tqdm import tqdm

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

def Testing(modelType, name, runs):
    
    # Load the model
    
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(MAX_STEPS, dtype=dtype)
    
    for run in range(runs): 
        
        print(f"====================== <{name} Testing, run: {run}> ======================")
        
        model = PPO.load(f"./Simulation/MachineLearning/Output/{name}")
        
        env = make_vec_env(SumoEnv, n_envs=1)

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

                data['AverageWaitTime'][step] += obs.item(0)
                data['AveragePeopleAtBusStops'][step] += obs.item(1)

                episode_starts = done

                step += 1
                pbar.update(1)

                if step==MAX_STEPS-1:
                    pbar.update(1)
                    pbar.close()

                if done.all():
                    print(f"Data before {data}")
                    env.close()

            del model

    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs

    print(f"Data after deviding by runs {data}")

    # Save the data to a CSV file
    TOCSV(data, name, "BothTesting")

    return data[:-1]


if __name__ == "__main__":
    ppo_data = Testing(PPO, "PPOBoth", 10)
    recurrentppo_data = Testing(RecurrentPPO, "Recurrent_PPOBoth", 10)
    trpo_data = Testing(TRPO, "TRPO", 10)


    PlotAverageWaitTimeMultiple(
        (ppo_data, "PPOBoth"), (recurrentppo_data, "Recurrent_PPOBoth"), (trpo_data, "TRPO"))
    

