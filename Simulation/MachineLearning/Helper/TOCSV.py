import csv
from os import mkdir, path
import os
import numpy as np


def TOCSV(data, name):
    if not os.path.isdir("./Simulation/MachineLearning/Output"):
        os.mkdir("./Simulation/MachineLearning/Output")
    if not os.path.isdir("./Simulation/MachineLearning/Output/TestFiles"):
        os.mkdir("./Simulation/MachineLearning/Output/TestFiles")

    np.savetxt(f"./Simulation/MachineLearning/Output/TestFiles/{name}.csv", data, delimiter=',',
               fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime")

