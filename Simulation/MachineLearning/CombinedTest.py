from PPOVersion import PPOVersion
from A2CVersion import A2CVersion
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple
from TRPOVersion import TRPOVersion
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion
import time


def CombinedTest():

    total_time = time.time()

    data_PPO = PPOVersion()

    data_A2C = A2CVersion()

    data_TRPO = TRPOVersion()

    data_random = RandomVersion()

    data_schedule = ScheduleVersion()

    data_greedy = GreedyFastVersion()

    print(f"Total time: {time.time() - total_time:.2f} seconds")

    PlotAverageWaitTimeMultiple(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO),
                                ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))

    PlotAveragePeopleAtBusstopsMultiple(("Random", data_random), ("Greedy", data_greedy), ("PPO", data_PPO),
                                        ("TRPO", data_TRPO), ("A2C", data_A2C), ("Schedule", data_schedule))


if __name__ == "__main__":
    CombinedTest()
