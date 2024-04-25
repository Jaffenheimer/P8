from random import randint
from stable_baselines3 import DDPG, HER, SAC, TD3, PPO, A2C
from sb3_contrib import QRDQN, TQC, ARS, RecurrentPPO, MaskablePPO
from stable_baselines3.common.env_util import make_vec_env
from SumoEnvironment import SumoEnv
import numpy as np
import Constants
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

#make a list of all the models

#HER is not a model anymore
#QRDQN did not work
#MaskablePPO did not work
# DDPG, ARS, TD3 is slow

MODELS = [SAC, PPO, TQC, A2C, RecurrentPPO]

#make association between a number in array and the model as a string:
ass = {0: "SAC", 1: "PPO", 2: "TQC", 3: "A2C", 4: "RecurrentPPO"}

def run(runs=1):
    # Importing the environment
    dataList = []
    for i,ml_model in enumerate(MODELS):
        env = make_vec_env(SumoEnv, n_envs=4)
        # Create the agent
        if i == 4:
            model = ml_model('MlpLstmPolicy',env, verbose=1)
        else:
            model = ml_model("MlpPolicy", env, verbose=1)

        # Train the agent
        model.learn(total_timesteps=Constants.TOTAL_TIMESTEPS, progress_bar=True)

        # Save the agent
        # model.save("ppo_sumo")

        # del model  # remove to demonstrate saving and loading

        # Load the trained agent
        # model = PPO.load("ppo_sumo")

        # Test the agent
        obs = env.reset()
        dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
        data = np.zeros(Constants.MAX_STEPS, dtype=dtype)
        
        for _ in range(runs):
            Constants.SEED = randint(0, 1000000)
            obs = env.reset()
            step = 0
            done = np.array([False], dtype='bool')

            while not done.all():
                action, _ = model.predict(obs)

                obs, rewards, done, info = env.step(action)
                data['AverageWaitTime'][step] = obs.item(0)
                data['AveragePeopleAtBusStops'][step] = obs.item(1)
                step += 1

                if done.all():
                    env.close()
                    
        newEntry = tuple()
        newEntry = (ass[i], data[:-1])
        dataList.append(newEntry)
        

    #pass the data as tuples with key as first value and the data as the second value, for all elems in dataList
    PlotAverageWaitTimeMultiple(dataList[0], dataList[1], dataList[2], dataList[3], dataList[4])
    
    PlotAveragePeopleAtBusstopsMultiple(dataList[0], dataList[1], dataList[2], dataList[3], dataList[4])
    
if __name__ == "__main__":
    run()