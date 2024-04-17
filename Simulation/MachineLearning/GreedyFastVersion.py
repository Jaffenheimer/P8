
from Helper.PlotDiagram import PlotOneAveragePeopleAtBusstops, PlotBoth, PlotAverageWaitTime
from Helper.CollectionData import average_people_at_busstops
from SumoEnviroment import SumoEnv
import asyncio
import traci
import numpy as np
from os import path, mkdir


def GreedyFastVersion(steps=1000):

    # Importing the environment
    env = SumoEnv()

    dtype = [ ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)

    step = 0
    obs = env.reset()
    while step < steps:
        action = [1, 1, 1, 1, 1]

        # Perform a step in the environment
        next_state, reward, done, info, truncated = env.step(action)
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = next_state.item(0)
        step += 1

    # Save the data to a CSV file
    if (path.isdir("../Output") == False):
        mkdir("../Output")
    np.savetxt(f"../Output/GreedyFastVersion.csv", data, delimiter=',',fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime") 

    # PlotAverageWaitTime(waiting_times_greedy_fast)
    # PlotOneAveragePeopleAtBusstops(people_at_busstops)
    # PlotBoth(waiting_times_greedy_fast, people_at_busstops)

    return data

