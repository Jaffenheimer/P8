
import matplotlib.pyplot as plt


def PlotAverageWaitTime(waiting_times):
    plt.figure(figsize=(10, 6))
    plt.plot(waiting_times, label="Average Waiting Time")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()


def PlotOneAveragePeopleAtBusstops(people_at_busstops):
    plt.figure(figsize=(10, 6))
    plt.plot(people_at_busstops, label="Average People at Busstops")
    plt.xlabel("Steps")
    plt.ylabel("Average People at Busstops")
    plt.title("Average People at Busstops Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()


def PlotBoth(waiting_times, people_at_busstops):
    # Create a figure with 2 rows and 1 column (2 subplots)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # Plot waiting times on the first subplot (ax1)
    ax1.plot(waiting_times, label="Average Waiting Time (s)")
    ax1.set_ylabel("Waiting Time (seconds)", color='blue')
    ax1.set_title("Average Waiting Time")
    ax1.grid(True)

    # Plot average people at bus stops on the second subplot (ax2)
    ax2.plot(people_at_busstops, label="Average People at Busstops", color='red')
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


def PlotCombinedAverageWaitTime(waiting_times_Random, waiting_times_greedy_fast, waiting_times_PPO, waiting_times_TRPO, waiting_times_A2C):
    plt.figure(figsize=(10, 6))
    plt.plot(waiting_times_Random, label="Random Version")
    plt.plot(waiting_times_greedy_fast, label="Greedy Fast Version")
    plt.plot(waiting_times_PPO, label="PPO Version")
    plt.plot(waiting_times_TRPO, label="TRPO Version")
    plt.plot(waiting_times_A2C, label="A2C Version")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()


def PlotCombinedAveragePeopleAtBusstops(people_at_busstops_Random, people_at_busstops_greedy_fast, people_at_busstops_times_PPO, people_at_busstops_times_TRPO, people_at_busstops_times_A2C):
    plt.figure(figsize=(10, 6))
    plt.plot(people_at_busstops_Random, label="Random Version")
    plt.plot(people_at_busstops_greedy_fast, label="Greedy Fast Version")
    plt.plot(people_at_busstops_times_PPO, label="PPO Version")
    plt.plot(people_at_busstops_times_TRPO, label="TRPO Version")
    plt.plot(people_at_busstops_times_A2C, label="A2C Version")
    plt.xlabel("Steps")
    plt.ylabel("Waiting Time (seconds)")
    plt.title("Average Waiting Time Over Testing Steps")
    plt.legend()
    plt.grid(True)
    plt.show()
