
import matplotlib.pyplot as plt


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
    plt.savefig('CombinedAverageWaitingTime.png')

# more dynamic, if you pass in a list of tuples with the first value being the name of the model and the second value being the data


def PlotAverageWaitTimeMultiple(*data):
    plt.figure(figsize=(10, len(data)))
    for i in data:
        plt.plot(i[1]['AverageWaitTime'], label=i[0])
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.savefig('CombinedAverageWaitingTime.png')
    plt.show()

# more dynamic, if you pass in a list of tuples with the first value being the name of the model and the second value being the data


def PlotAveragePeopleAtBusstopsMultiple(*data):
    plt.figure(figsize=(10, len(data)))
    for i in data:
        plt.plot(i[1]['AveragePeopleAtBusStops'], label=i[0])
    plt.xlabel("Steps")
    plt.ylabel("Average People at Busstops")
    plt.title("Average People at Busstops Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.savefig('CombinedAveragePeopleAtBusstops.png')
    plt.show()


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
    plt.savefig('CombinedAveragePeopleAtBusstops.png')
