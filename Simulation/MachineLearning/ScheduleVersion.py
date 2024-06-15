import os
from Helper.FindAverage import findAverageWaitTime
import traci
import numpy as np
from os import path, mkdir
from Constants import SCHEDULE_MAX_STEPS, SEED, INPUTFILE, SUMO_INIT_STEPS, SEEDS, INPUTFILE


def ScheduleVersion(inputFile=f"../P8-Mobility/Simulation/SUMO/schedule/{INPUTFILE}", outputFileName="Schedule.csv"):
    # initializations

    print("====================== <Schedule Init> ======================")

    dtype = [('AveragePeopleAtBusStops', float),
             ('AverageWaitTime', float)]
    data = np.zeros(SCHEDULE_MAX_STEPS, dtype=dtype)
    # Connect to SUMO simulation
    try:
        traci.close()
    except:
        pass
    traci.start(["sumo", "-c", path.abspath(inputFile), "--seed", str(SEED), "--no-warnings"])

    # simulation loop
    step = 0

    personsWaitingTimeList = []

    while step < SCHEDULE_MAX_STEPS+SUMO_INIT_STEPS:
        while step < SUMO_INIT_STEPS:
            traci.simulationStep()
            step += 1

        
        traci.simulationStep()

        persons = traci.person.getIDList()
            
        averageWaitTime = getAverageWaitTime(persons)
        averagePeopleAtBusStops = getAveragePeopleAtBusStops()

        # print(f"Step: {step} - AverageWaitTime: {averageWaitTime}, AveragePeopleAtBusStops: {averagePeopleAtBusStops}, Persons: {len(persons)}")
        # print(f"-----------------------------------------------------------------------------------------------------")

        data['AveragePeopleAtBusStops'][step-SUMO_INIT_STEPS] = averagePeopleAtBusStops
        data['AverageWaitTime'][step-SUMO_INIT_STEPS] = averageWaitTime

        personsWaitingTimeList.clear()
        step += 1
    traci.close()

    if not os.path.isdir("./Simulation/MachineLearning/Output/TestFiles"):
        os.mkdir("./Simulation/MachineLearning/Output/TestFiles")

    np.savetxt(f"./Simulation/MachineLearning/Output/TestFiles/{outputFileName}", data, delimiter=',',
            fmt='%f', header="AveragePeopleAtBusStops,AverageWaitTime")

    print("====================== <Schedule Done> ======================")

    return data[:-1]


def getAverageWaitTime(persons):
    personsWaitingTimeList = []
    numOfPersons = len(persons)
    for j in range(numOfPersons):
        personWaitingTime = traci.person.getWaitingTime(persons[j])
        personsWaitingTimeList.append(personWaitingTime)

    # finds average wait time
    length = len(personsWaitingTimeList)
    averageWaitTime = sum(personsWaitingTimeList)/length if length != 0 else 0
    return averageWaitTime


def getAveragePeopleAtBusStops():
    busStops = traci.busstop.getIDList()
    totalPeopleAtBusStops = 0
    for busStop in busStops:
        totalPeopleAtBusStops += traci.busstop.getPersonCount(busStop)
    return totalPeopleAtBusStops/len(busStops)


# now for multiple runs, where the values are the average of the runs:


def ScheduleVersionMultiple(runs=1, outputFileName="output.csv"):
    dtype = [('AverageWaitTime', float)]
    data = np.zeros(SCHEDULE_MAX_STEPS, dtype=dtype)
    seeds = SEEDS[:]
    filePath = path.abspath(f"../P8-Mobility/Simulation/SUMO/algorithm/{INPUTFILE}")
    for run in range(runs):
        # Connect to SUMO simulation
        print("running with Schedule with seed: ", seeds[0])
        traci.start(
            ["sumo", "-c", path.abspath(filePath), "--seed", str(seeds.pop(0)), "--no-warnings"])
        seeds.pop(0)
        # simulation loop
        step = 0
        while step < SCHEDULE_MAX_STEPS:
            traci.simulationStep()

            persons = traci.person.getIDList()

            averageWaitTime = getAverageWaitTime(persons)
            data['AverageWaitTime'][step] += averageWaitTime

            step += 1
        traci.close()
    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    if (path.isdir("./Simulation/MachineLearning/Output/TestFiles") == False):
        mkdir("./Simulation/MachineLearning/Output/TestFiles")
    np.savetxt(f"./Simulation/MachineLearning/Output/TestFiles/{outputFileName}", data, delimiter=',',
               fmt='%f', header="AverageWaitTime")
    return data


if __name__ == "__main__":
    data = ScheduleVersionMultiple(5, "Schedule.csv")  
    findAverageWaitTime(("Schedule",data))
