import asyncio
from PPOVersion import PPOVersion
from A2CVersion import A2CVersion
from Helper.PlotDiagram import PlotCombinedAverageWaitTime, PlotCombinedAveragePeopleAtBusstops
from TRPOVersion import TRPOVersion
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion


def CombinedTest():
    # Load the data
    total_timesteps = 500
    steps = 1000

    # PPO SUMO TRAINING
    data_PPO = PPOVersion(total_timesteps, steps)
    print("PPO done")

    # A2C SUMO TRAINING
    data_A2C =  A2CVersion(total_timesteps, steps)
    print("A2C done")

    # # TRPO SUMO TRAINING
    data_TRPO = TRPOVersion(total_timesteps, steps)
    print("TRPO done")

    # Random SUMO TRAINING
    data_random = RandomVersion(steps)
    print("Random done")
    
    # Schedule SUMO TRAINING
    data_schedule = ScheduleVersion(steps=steps)
    print("Schedule done")

    # Greedy Fast SUMO TRAINING
    data_greedy = GreedyFastVersion(steps)
    print("Greedy Fast done")

    PlotCombinedAverageWaitTime(data_random['AverageWaitTime'], data_greedy['AverageWaitTime'], data_PPO['AverageWaitTime'],
                                      data_TRPO['AverageWaitTime'], data_A2C['AverageWaitTime'], data_schedule['AverageWaitTime'])
    
    PlotCombinedAveragePeopleAtBusstops(data_random['AveragePeopleAtBusStops'], data_greedy['AveragePeopleAtBusStops'],
                                         data_PPO['AveragePeopleAtBusStops'], data_TRPO['AveragePeopleAtBusStops'], data_A2C['AveragePeopleAtBusStops'], data_schedule['AveragePeopleAtBusStops'])


CombinedTest()