
from Helper.PlotDiagram import PlotOneAveragePeopleAtBusstops, PlotBoth, PlotAverageWaitTime
from Helper.CSVWriter import CSVWriter
from Helper.CollectionData import avarage_people_at_busstops
from SumoEnviroment import SumoEnv
import asyncio
import traci


async def GreedyFastVersion(steps=1000):

    # Importing the environment
    env = SumoEnv()

    waiting_times_greedy_fast = []  # List to store average waiting time at each step
    people_at_busstops = []

    step = 0
    obs = env.reset()
    while step < steps:
        action = [1, 1, 1, 1, 1]

        # Perform a step in the environment
        next_state, reward, done, info, truncated = env.step(action)
        people_at_busstops.append(avarage_people_at_busstops())
        waiting_times_greedy_fast.append(next_state.item(0))
        step += 1

    # Save the data to a CSV file
    newList = []
    newList.append(waiting_times_greedy_fast)
    newList.append(people_at_busstops)
    CSVWriter(newList,
              "GreedyFastVersion.csv", ["Waiting Times", "Average People at Busstops"])

    # PlotAverageWaitTime(waiting_times_greedy_fast)
    # PlotOneAveragePeopleAtBusstops(people_at_busstops)
    # PlotBoth(waiting_times_greedy_fast, people_at_busstops)

    return waiting_times_greedy_fast, people_at_busstops

asyncio.run(GreedyFastVersion())
