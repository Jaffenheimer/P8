import Helper.SeedGenerator as sg

MAX_STEPS = 100

PEEK_INTERVAL = 50
PEEK_LEARN_STEPS = 50


RANDOM_MAX_STEPS = MAX_STEPS
SCHEDULE_MAX_STEPS = MAX_STEPS
GREEDY_MAX_STEPS = MAX_STEPS

# These should be lower or equal to the MAX LEARN STEPS ()
A2C_MAX_STEPS = MAX_STEPS
PPO_MAX_STEPS = MAX_STEPS
TRPO_MAX_STEPS = MAX_STEPS


TOTAL_TIMESTEPS = 1200
A2C_TOTAL_TIMESTEPS = TOTAL_TIMESTEPS
PPO_TOTAL_TIMESTEPS = TOTAL_TIMESTEPS
TRPO_TOTAL_TIMESTEPS = TOTAL_TIMESTEPS

SUMO_INIT_STEPS = 200

SEED = sg.SEED

REWARD_THRESHOLD = 500
