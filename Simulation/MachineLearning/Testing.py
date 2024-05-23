from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from sb3_contrib import RecurrentPPO, TRPO
from SumoEnvironmentTesting import SumoEnv
from Helper.TOCSV import TOCSV
from Constants import MAX_STEPS
from Helper.PlotDiagram import PlotAverageWaitTimeMultiple
from Helper.FindAverage import findAverageWaitTime

import numpy as np
from tqdm import tqdm

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

def Testing(modelType, name, runs):
    
    # Load the model
    
    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(MAX_STEPS, dtype=dtype)
    
    env = make_vec_env(SumoEnv, n_envs=1)
    for run in range(runs): 
        
        print(f"====================== <{name} Testing, run: {run}> ======================")
        
        model = modelType.load(f"./Simulation/MachineLearning/input/{name}")
        

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
                    env.close()

            del model
            lstm_states = None
            episode_starts = np.ones((1,), dtype=bool)

    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs

    # Save the data to a CSV file
    TOCSV(data, name)

    return data[:-1]


if __name__ == "__main__":
    A2C_low = Testing(A2C, "A2C_low", 5)
    A2C_high = Testing(A2C, "A2C_high", 5)
    A2C_both = Testing(A2C, "A2C_both", 5)


    PlotAverageWaitTimeMultiple(
        ("A2C_low",A2C_low), ("A2C_high",A2C_high), ("A2C_both",A2C_both))
    
    findAverageWaitTime(("A2C_low",A2C_low), ("A2C_high",A2C_high), ("A2C_both",A2C_both))
    

