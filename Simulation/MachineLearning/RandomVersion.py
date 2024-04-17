
from SumoEnviroment import SumoEnv
from Helper.CollectionData import avarage_people_at_busstops
import random
import asyncio


async def RandomVersion(steps=1000):

    # Importing the environment
    env = SumoEnv()

    waiting_times_Random = []
    people_at_busstops = []
    step = 0
    obs = env.reset()

    while step < steps:
        action = [random.randint(-1, 1) for i in range(5)]

        # Perform a step in the environment
        next_state, reward, done, info, truncated = env.step(action)
        waiting_times_Random.append(next_state.item(0))
        people_at_busstops.append(avarage_people_at_busstops())
        step += 1

    return waiting_times_Random, people_at_busstops

asyncio.run(RandomVersion())
