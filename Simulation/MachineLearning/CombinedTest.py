import asyncio
from PPOVersion import PPOVersion
from A2CVersion import A2CVersion
from Helper.PlotDiagram import PlotCombinedAverageWaitTime, PlotCombinedAveragePeopleAtBusstops
from TRPOVersion import TRPOVersion
from RandomVersion import RandomVersion
from GreedyFastVersion import GreedyFastVersion


async def CombinedTest():
    # Load the data
    total_timesteps = 20000
    steps = 2000

    # PPO SUMO TRAINING
    watingtime_ppo, busstops_ppo = await PPOVersion(total_timesteps, steps)
    print("PPO done")

    # A2C SUMO TRAINING
    watingtime_a2c, busstops_a2c = await A2CVersion(total_timesteps, steps)
    print("A2C done")

    # # TRPO SUMO TRAINING
    watingtime_trpo, busstops_trpo = await TRPOVersion(total_timesteps, steps)
    print("TRPO done")

    # Random SUMO TRAINING
    watingtime_random, busstops_random = await RandomVersion(steps)
    print("Random done")

    # Greedy Fast SUMO TRAINING
    watingtime_greedy_fast, busstops_greedy_fast = await GreedyFastVersion(steps)
    print("Greedy Fast done")

    await PlotCombinedAverageWaitTime(watingtime_random, watingtime_greedy_fast,
                                      watingtime_ppo, watingtime_trpo, watingtime_a2c)

    PlotCombinedAveragePeopleAtBusstops(
        busstops_random, busstops_greedy_fast, busstops_ppo, busstops_trpo, busstops_a2c)


# Run the async function within an event loop
asyncio.run(CombinedTest())
