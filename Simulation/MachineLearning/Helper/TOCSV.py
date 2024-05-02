import csv
from pathlib import Path
import os
import numpy as np


def TOCSV(data, name, version=""):

    if not os.path.isdir("./Simulation/MachineLearning/Output"):
        os.mkdir("./Simulation/MachineLearning/Output")

    if not os.path.isdir("./Simulation/MachineLearning/Output/TestFiles"):
        os.mkdir("./Simulation/MachineLearning/Output/TestFiles")

    np.savetxt(f"./Simulation/MachineLearning/Output/TestFiles/{version}{name}.csv", data, delimiter=',',
               fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime")

