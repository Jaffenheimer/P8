from stable_baselines3 import PPO, A2C
from sb3_contrib import RecurrentPPO, TRPO
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion
import time
import ModelPeek
from Helper.FindAverage import FindAverage

def CombinedTest():

    start_time = time.time()

    data_PPO = ModelPeek.run(PPO, "PPO", "MlpPolicy")
    
    data_recurrent_PPO = ModelPeek.run(RecurrentPPO, "Recurrent PPO", "MlpLstmPolicy")

    data_A2C = ModelPeek.run(A2C, "A2C", "MlpPolicy")

    data_TRPO = ModelPeek.run(TRPO, "TRPO", "MlpPolicy")

    data_random = RandomVersion()

    data_schedule = ScheduleVersion()

    data_greedy = GreedyFastVersion()

    print(f"Total time: {time.time() - start_time:.2f} seconds")

    FindAverage(data_PPO, data_recurrent_PPO, data_A2C, data_TRPO,
                data_random, data_schedule, data_greedy)

    PlotAverageWaitTimeMultiple("CombinedPeek", ("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
                                ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))

    PlotAveragePeopleAtBusstopsMultiple("CombinedPeek", ("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO), ("Recurrent PPO", data_recurrent_PPO),
                                        ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))


if __name__ == "__main__":
    CombinedTest()
