import Helper.SeedGenerator as sg
import multiprocessing
from random import randint

# TOTAL_TIMESTEPS / (MAX_STEPS * N_ENVS) must be an integer
TOTAL_TIMESTEPS = 10
MAX_STEPS = 40
N_ENVS = 4 # MAX (amout of core - 1)

RANDOM_MAX_STEPS = MAX_STEPS
SCHEDULE_MAX_STEPS = MAX_STEPS
GREEDY_MAX_STEPS = MAX_STEPS

UPDATEPOLICY = 200

SUMO_INIT_STEPS = 200

SEED = sg.SEED
SEEDS = [18467,0, 66312,0, 28134,0, 17258,0, 50199,0,0,0]

REWARD_THRESHOLD = 500

INPUTFILE = "low_traffic.sumocfg"