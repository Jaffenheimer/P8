import numpy as np
from stable_baselines3 import PPO, A2C
from sb3_contrib import RecurrentPPO, TRPO
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple
from RandomVersion import RandomVersion
from Helper.FindAverage import FindAverage
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion
import time
import Model


def CombinedTest():

    start_time = time.time()

    data_PPO = Model.run(PPO, "PPO", "MlpPolicy")

    data_recurrent_PPO = Model.run(
        RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")

    data_A2C = Model.run(A2C, "A2C", "MlpPolicy")

    data_TRPO = Model.run(TRPO, "TRPO", "MlpPolicy")

    data_random = RandomVersion()

    data_schedule = ScheduleVersion()

    data_greedy = GreedyFastVersion()

    print(f"Total time: {time.time() - start_time:.2f} seconds")

    FindAverage(data_PPO, data_recurrent_PPO, data_A2C, data_TRPO,
                data_random, data_schedule, data_greedy)
        
    PlotAverageWaitTimeMultiple(("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO), ("A2C", data_A2C), ("TRPO", data_TRPO), ("Random", data_random), ("Greedy Fast", data_greedy))

    PlotAveragePeopleAtBusstopsMultiple(("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO), ("A2C", data_A2C), ("TRPO", data_TRPO), ("Random", data_random), ("Greedy Fast", data_greedy))

if __name__ == "__main__":
    CombinedTest()
