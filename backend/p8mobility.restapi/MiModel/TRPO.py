from sb3_contrib import TRPO
import os

import numpy as np

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")


def Testing(obs):
    # Load the model

    obs = np.fromstring(obs, dtype=np.float32, sep=',')
    
    model = TRPO.load("C:/Users/jjtor/source/repos/P8-Mobility/backend/p8mobility.restapi/MiModel/TRPO_high.zip")

    action, _states = model.predict(obs)

    #print(action, _states)

    return action

def main():

    obs = os.sys.argv[1]

    # read obs from argv[1]
    return Testing(obs)

if __name__ == "__main__":

    action = main()

    print(action)
    
        
        