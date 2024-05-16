from stable_baselines3 import TRPO
import os, process

import numpy as np

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")


def Testing(obs):
    # Load the model

    obs = np.array(obs.split(",")).astype(np.float32)

    model = TRPO.load("./TRPO_High.zip")

    action, _ = model.predict(obs)

    return action

def main():
    # read obs from argv[1]
    return Testing(os.sys.argv[1])

if __name__ == "__main__":
    print("I started and received ")
    print(os.sys.argv)

    action = main()
    with open("/Users/jonathanwisborgfog/Documents/8.Semester/projekt/P8-Mobility/backend/p8mobility.restapi/MiModel/action.txt", "w") as f:
        f.write(action.join(","))
    print("I finished")
    print(action)
    
        
        