from PPOPeekVersion import PPOPeekVersion
from A2CPeekVersion import A2CPeekVersion
from Helper.PlotDiagram import PlotAveragePeopleAtBusstopsMultiple, PlotAverageWaitTimeMultiple
from TRPOPeekVersion import TRPOPeekVersion
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion
from ScheduleVersion import ScheduleVersion

def CombinedPeekTest():

    data_PPO = PPOPeekVersion()
    print("PPO done")

    data_A2C = A2CPeekVersion()
    print("A2C done")

    data_TRPO = TRPOPeekVersion()
    print("TRPO done")

    data_random = RandomVersion()
    print("Random done")

    data_schedule = ScheduleVersion()
    print("Schedule done")

    data_greedy = GreedyFastVersion()
    print("Greedy Fast done")
    
    PlotAverageWaitTimeMultiple(("Random",data_random),("Greedy",data_greedy), ("PPO",data_PPO),
                                ("TRPO",data_TRPO), ("A2C",data_A2C), ("Schedule",data_schedule))

    PlotAveragePeopleAtBusstopsMultiple(("Random",data_random),("Greedy",data_greedy), ("PPO",data_PPO),
                                ("TRPO",data_TRPO), ("A2C",data_A2C), ("Schedule",data_schedule))

if __name__ == "__main__":
    CombinedPeekTest()
