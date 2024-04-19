from PPOVersion import PPOVersion
from A2CVersion import A2CVersion
from Helper.PlotDiagram import PlotCombinedAverageWaitTime, PlotCombinedAveragePeopleAtBusstops
from TRPOVersion import TRPOVersion
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion

def CombinedTest():

    data_PPO = PPOVersion()
    print("PPO done")

    data_A2C = A2CVersion()
    print("A2C done")

    data_TRPO = TRPOVersion()
    print("TRPO done")

    data_random = RandomVersion()
    print("Random done")

    data_schedule = ScheduleVersion()
    print("Schedule done")

    data_greedy = GreedyFastVersion()
    print("Greedy Fast done")

    PlotCombinedAverageWaitTime(data_random['AverageWaitTime'], data_greedy['AverageWaitTime'], data_PPO['AverageWaitTime'],
                                data_TRPO['AverageWaitTime'], data_A2C['AverageWaitTime'], data_schedule['AverageWaitTime'])

    PlotCombinedAveragePeopleAtBusstops(data_random['AveragePeopleAtBusStops'], data_greedy['AveragePeopleAtBusStops'],
                                        data_PPO['AveragePeopleAtBusStops'], data_TRPO['AveragePeopleAtBusStops'], data_A2C['AveragePeopleAtBusStops'], data_schedule['AveragePeopleAtBusStops'])


CombinedTest()
