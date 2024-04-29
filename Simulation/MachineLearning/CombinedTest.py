import numpy as np
from stable_baselines3 import PPO, A2C
from sb3_contrib import RecurrentPPO, TRPO
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple, PlotAverageWaitTimeMultipleOld, PlotAveragePeopleAtBusstopsMultipleOld
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
    
    PlotAverageWaitTimeMultiple(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
                                ("TRPO", data_TRPO), ("A2C", data_A2C))
    

    PlotAveragePeopleAtBusstopsMultiple(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
                                        ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))

    # Old plots for comparison    
    # PlotAverageWaitTimeMultipleOld(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
    #                                ("TRPO", data_TRPO), ("A2C", data_A2C))
    
    # PlotAveragePeopleAtBusstopsMultipleOld(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
    #                                     ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))


if __name__ == "__main__":
    CombinedTest()

    # dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    # data_array = np.zeros(10000, dtype=dtype)

    # for i in range(9999):
    #     data_array['AveragePeopleAtBusStops'][i] = i*0.5
    #     data_array['AverageWaitTime'][i] = i*0.5
    
    # np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
    # print(data_array)

    # PlotAverageWaitTimeMultiple(("Random", data_array))
