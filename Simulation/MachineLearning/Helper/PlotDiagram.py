
from os import mkdir, path
import matplotlib.pyplot as plt
import numpy as np
from Constants import MAX_STEPS

def PlotAverageWaitTime(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['AverageWaitTime'], label="Average Waiting Time")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()


def PlotOneAveragePeopleAtBusstops(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['AverageWaitTime'],
             label="Average People at Busstops")
    plt.xlabel("Steps")
    plt.ylabel("Average People at Busstops")
    plt.title("Average People at Busstops Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()


def PlotBoth(data):
    # Create a figure with 2 rows and 1 column (2 subplots)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # Plot waiting times on the first subplot (ax1)
    ax1.plot(data['AverageWaitTime'], label="Average Waiting Time (s)")
    ax1.set_ylabel("Waiting Time (seconds)", color='blue')
    ax1.set_title("Average Waiting Time")
    ax1.grid(True)

    # Plot average people at bus stops on the second subplot (ax2)
    ax2.plot(data['AveragePeopleAtBusStops'],
             label="Average People at Busstops", color='red')
    ax2.set_ylabel("People at Busstops", color='red')
    ax2.set_xlabel("Steps")
    ax2.grid(True)

    # Set common title for the entire figure (optional)
    fig.suptitle(
        "Average Waiting Time & People at Busstops Over Testing Steps")

    # Add a legend to the entire figure (optional)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(lines1 + lines2, labels1 + labels2, loc='upper center',
               bbox_to_anchor=(0.5, 1.15))

    plt.tight_layout()
    plt.show()


def PlotCombinedAverageWaitTime(Random, greedy_fast, PPO, TRPO, A2C, Schedule):
    plt.figure(figsize=(10, 6))
    plt.plot(Random, label="Random Version")
    plt.plot(greedy_fast, label="Greedy Fast Version")
    plt.plot(PPO, label="PPO Version")
    plt.plot(TRPO, label="TRPO Version")
    plt.plot(A2C, label="A2C Version")
    plt.plot(Schedule, label="Schedule Version")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    # plt.show()
    if not path.isdir("./Simulation/MachineLearning/Output"):
        mkdir("./Simulation/MachineLearning/Output")
    plt.savefig(
        './Simulation/MachineLearning/Output/CombinedAverageWaitingTime.png')

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
                f"Average Waiting Time (low) (every {step_factor} steps)")
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
    #plt.show()

# more dynamic, if you pass in a list of tuples with the first value being the name of the model and the second value being the data


def PlotAveragePeopleAtBusstopsMultiple(name, *data):
    plt.figure(figsize=(15, 6))
    
    for index, i in enumerate(data):
        colors = plt.cm.get_cmap('tab10')
        if MAX_STEPS >= 1000:
            step_factor = MAX_STEPS // 200
            pl_data = i[1]['AveragePeopleAtBusStops'][::step_factor]
            list_length = len(pl_data)
            x = [step_factor * step for step in range(0, list_length)]

            plt.plot(x, pl_data, label=i[0], color=colors(index % len(data)))
            plt.title(f"Average People at Busstops Over Testing (every {step_factor} steps) [{name}] ")
        else:
            plt.plot(i[1]['AveragePeopleAtBusStops'],
                     label=i[0], color=colors(index % len(data)))
            plt.title(
                f"Average People at Busstops (every step) [{name}]")

    plt.xlabel("Steps")
    plt.ylabel("Average People at Busstops")
    plt.legend()
    plt.grid(True)

    if not path.isdir("./Simulation/MachineLearning/Output"):
        mkdir("./Simulation/MachineLearning/Output")
    plt.savefig(
        f'./Simulation/MachineLearning/Output/CombinedAveragePeopleAtBusstops{name}.png', dpi=1200)
    # plt.show()



def PlotCombinedAveragePeopleAtBusstops(Random, greedy_fast, PPO, TRPO, A2C, Schedule):
    plt.figure(figsize=(10, 6))
    plt.plot(Random, label="Random Version")
    plt.plot(greedy_fast, label="Greedy Fast Version")
    plt.plot(PPO, label="PPO Version")
    plt.plot(TRPO, label="TRPO Version")
    plt.plot(A2C, label="A2C Version")
    plt.plot(Schedule, label="Schedule Version")
    plt.xlabel("Steps")
    plt.ylabel("Average People at Busstops")
    plt.title("Average People at Busstops Over Testing Steps")
    plt.legend()
    plt.grid(True)
    # plt.show()
    if not path.isdir("./Simulation/MachineLearning/Output"):
        mkdir("./Simulation/MachineLearning/Output")
    plt.savefig(
        './Simulation/MachineLearning/Output/CombinedAveragePeopleAtBusstops.png')
