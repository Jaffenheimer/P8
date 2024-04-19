
from SumoEnviroment import SumoEnv
from Helper.CollectionData import average_people_at_busstops
import random
import numpy as np
from Constants import RANDOM_MAX_LEARN_STEPS


def RandomVersion():

    # Importing the environment
    env = SumoEnv()

    dtype = [('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(RANDOM_MAX_LEARN_STEPS, dtype=dtype)

    step = 0
    obs = env.reset()

    done = np.array([False], dtype='bool')

    while not done:
        action = [random.randint(-1, 1) for i in range(5)]

        # Perform a step in the environment
        next_state, reward, done, info, truncated = env.step(action)
        data['AveragePeopleAtBusStops'][step] = average_people_at_busstops()
        data['AverageWaitTime'][step] = next_state.item(0)
        step += 1

        print(f"Step: {step}, done: {done}, rewards: {reward}, info: {info}")

        if done:
            env.close()

    return data


RandomVersion()