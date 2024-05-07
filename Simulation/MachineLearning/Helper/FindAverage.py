import os
import numpy as np


def FindAverage(data_PPO, data_recurrent_PPO, data_A2C, data_TRPO, data_random, data_schedule, data_greedy):
    """
    Find the average of the data for each model
    """

    np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

    # Waiting time
    average_wait_time_PPO = np.average(data_PPO['AverageWaitTime'])
    average_wait_time_recurrent_PPO = np.average(
        data_recurrent_PPO['AverageWaitTime'])
    average_wait_time_A2C = np.average(data_A2C['AverageWaitTime'])
    average_wait_time_TRPO = np.average(data_TRPO['AverageWaitTime'])
    average_wait_time_random = np.average(data_random['AverageWaitTime'])
    average_wait_time_schedule = np.average(data_schedule['AverageWaitTime'])
    average_wait_time_greedy = np.average(data_greedy['AverageWaitTime'])

    # People at bus stops
    average_people_PPO = np.average(data_PPO['AveragePeopleAtBusStops'])
    average_people_recurrent_PPO = np.average(
        data_recurrent_PPO['AveragePeopleAtBusStops'])
    average_people_A2C = np.average(data_A2C['AveragePeopleAtBusStops'])
    average_people_TRPO = np.average(data_TRPO['AveragePeopleAtBusStops'])
    average_people_random = np.average(data_random['AveragePeopleAtBusStops'])
    average_people_schedule = np.average(
        data_schedule['AveragePeopleAtBusStops'])
    average_people_greedy = np.average(data_greedy['AveragePeopleAtBusStops'])

    directory = "./Simulation/MachineLearning/Output"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "AverageData.csv")


    modelAverage = (average_wait_time_PPO+average_wait_time_recurrent_PPO+average_wait_time_A2C+average_wait_time_TRPO)/4
    print(f"Average waittime for all models: {modelAverage:.2f}\n")


    # Print the result to csv
    with open(file_path, 'w') as f:
        f.write("Model,Average Wait Time,Average People at Bus Stops\n")
        f.write(f"Average waittime for all models: {modelAverage:.2f}\n")
        f.write(f"PPO,{average_wait_time_PPO:.2f},{average_people_PPO:.2f}\n")
        f.write(
            f"Recurrent PPO,{average_wait_time_recurrent_PPO:.2f},{average_people_recurrent_PPO:.2f}\n")
        f.write(f"A2C,{average_wait_time_A2C:.2f},{average_people_A2C:.2f}\n")
        f.write(
            f"TRPO,{average_wait_time_TRPO:.2f},{average_people_TRPO:.2f}\n")
        f.write(
            f"Random,{average_wait_time_random:.2f},{average_people_random:.2f}\n")
        f.write(
            f"Schedule,{average_wait_time_schedule:.2f},{average_people_schedule:.2f}\n")
        f.write(
            f"Greedy,{average_wait_time_greedy:.2f},{average_people_greedy:.2f}\n")



def FindAverage1(data): 
    np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

    average_wait_time = np.average(data['AverageWaitTime'])

    directory = "./Simulation/MachineLearning/Output"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "AverageDataDATA.csv")

    with open(file_path, 'w') as f:
        f.write("Model,Average Wait Time\n")
        f.write(f"Average waittime,{average_wait_time:.2f}\n")



