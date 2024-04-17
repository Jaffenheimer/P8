
from SumoEnviroment import SumoEnv
from Helper.CollectionData import average_people_at_busstops
import random
import asyncio
import numpy as np


def RandomVersion(steps=1000):

    # Importing the environment
    env = SumoEnv()

    dtype = [ ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)

    step = 0
    obs = env.reset()

    while step < steps:
        action = [random.randint(-1, 1) for i in range(5)]

        # Perform a step in the environment
        next_state, reward, done, info, truncated = env.step(action)
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = next_state.item(0)
        step += 1

    return data

