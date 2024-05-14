import csv
from pathlib import Path
import os
import numpy as np


def TOCSV(data, name):
    if not os.path.isdir("./Simulation/MachineLearning/Output"):
        os.mkdir("./Simulation/MachineLearning/Output")
    if not os.path.isdir("./Simulation/MachineLearning/Output/TestFiles"):
        os.mkdir("./Simulation/MachineLearning/Output/TestFiles")

    np.savetxt(f"./Simulation/MachineLearning/Output/TestFiles/{name}.csv", data, delimiter=',',
               fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime")

def RUNNING_TOCSV(data):
    mypath = os.path.abspath(os.getcwd()).replace("\\", "/")
    if not os.path.isdir(f"{mypath}/Simulation/MachineLearning/Output"):
        os.mkdir(f"{mypath}/Simulation/MachineLearning/Output")
    
    # If the data is all zeros, then clear run.csv
    if (np.all(data == 0.0)):
        with open(f"{mypath}/Simulation/MachineLearning/Output/run.csv", 'w') as f:
            pass

    with open(f"{mypath}/Simulation/MachineLearning/Output/run.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        _data = data.tolist()[0]
        if (np.all(data == 0.0)):
            writer.writerow(["average_wait_time", "average_people_at_busstops", 
                                "bus0_speed", "bus0_position", 
                                "bus1_speed", "bus1_position", 
                                "bus2_speed", "bus2_position", 
                                "bus3_speed", "bus3_position", 
                                "bus4_speed", "bus4_position"])
        writer.writerow(_data)