
from os import mkdir, path
import matplotlib.pyplot as plt
import numpy as np
from Constants import MAX_STEPS
import glob
from pathlib import Path

def PlotAverageWaitTime(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['AverageWaitTime'], label="Average Waiting Time")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()




# more dynamic, if you pass in a list of tuples with the first value being the name of the model and the second value being the data
def PlotAverageWaitTimeMultiple(*data):
    plt.figure(figsize=(15, 6))

    for index, i in enumerate(data):
        colors = plt.cm.get_cmap('tab10')
        if MAX_STEPS >= 1000:
            step_factor = MAX_STEPS // 200
            pl_data = i[1]['AverageWaitTime'][::step_factor]
            list_length = len(pl_data)
            x = [step_factor * step for step in range(0, list_length)]
            
            plt.plot(x, pl_data ,label=i[0], color=colors(index % len(data)))
            plt.title(
                f"Average Waiting Time (high) (every {step_factor} steps)")
        else:
            plt.plot(i[1]['AverageWaitTime'], label=i[0], color=colors(index % len(data)))
            plt.title(
                f"Average Waiting Time (low) (every step)")


    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.legend()
    plt.grid(True)

    if not path.isdir("./Simulation/MachineLearning/Output"):
        mkdir("./Simulation/MachineLearning/Output")
    plt.savefig(
        f'./Simulation/MachineLearning/Output/CombinedAverageWaitingTime.png', dpi=1200)
    # plt.show()

def plotFromCSV():
    allData = []
    for filePath in glob.glob(path.abspath("Simulation/MachineLearning/Input/csvFiles/*.csv")):
        name = Path(filePath).stem
        dtype = [('AverageWaitTime', float)]
        data = np.zeros(MAX_STEPS, dtype=dtype)
        for i,line in enumerate(open(filePath, "r")):
            if i == 0:
                continue
            if i == MAX_STEPS:
                continue
            if ',' in line:
                data['AverageWaitTime'][i] = line.split(",")[1]
            else:
                data['AverageWaitTime'][i] = line
        allData.append( (name,data) )
    PlotAverageWaitTimeMultiple(*allData)
        