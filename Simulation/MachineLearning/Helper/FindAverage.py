import os
import numpy as np

#more dynamic version
def findAverageWaitTime(*allData):
    waitTimes = {}
    for i,data in enumerate(allData):
        waitTimes[data[0]] = np.average(data[1]['AverageWaitTime'])
    
    directory = "./Simulation/MachineLearning/Output"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "AverageData.csv")

    with open(file_path, 'w') as f:
        f.write("Model,Average Wait Time\n")
        for key, value in waitTimes.items():
            f.write(f"{key},{value:.2f}\n")