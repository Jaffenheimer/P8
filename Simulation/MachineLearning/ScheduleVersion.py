import traci
import numpy as np
from os import path, mkdir
from Constants import SCHEDULE_MAX_STEPS, SEED
from Helper.PlotDiagram import PlotBoth


def ScheduleVersion(inputFile="../P8-Mobility/Simulation/SUMO/schedule/high_person_low_traffic.sumocfg", outputFileName="output_schedule.csv"):
    # initializations

    print("====================== <Schedule Init> ======================")

    dtype = [('Step', int), ('AveragePeopleAtBusStops', float),
             ('AverageWaitTime', float)]
    data = np.zeros(SCHEDULE_MAX_STEPS, dtype=dtype)
    # Connect to SUMO simulation
    try:
        traci.close()
    except:
        pass
    traci.start(["sumo", "-c", path.abspath(inputFile), "--seed", str(SEED)])

    # simulation loop
    step = 0
    while step < SCHEDULE_MAX_STEPS:
        traci.simulationStep()

        persons = traci.person.getIDList()

        averageWaitTime = getAverageWaitTime(persons)
        averagePeopleAtBusStops = getAveragePeopleAtBusStops()

        data['Step'][step] = step
        data['AveragePeopleAtBusStops'][step] = averagePeopleAtBusStops
        data['AverageWaitTime'][step] = averageWaitTime

        step += 1
    traci.close()
    if (path.isdir("../Output") == False):
        mkdir("../Output")
    np.savetxt(f"../Output/{outputFileName}", data, delimiter=',',
               fmt='%f', header="Step,AveragePeopleAtBusStops,AverageWaitTime")

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


def ScheduleVersionMultiple(runs=1, inputFile="../P8-Mobility/Simulation/SUMO/schedule/high_person_low_traffic.sumocfg", outputFileName="output.csv"):
    dtype = [('Step', int), ('PedestrianCount', float),
             ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(SCHEDULE_MAX_STEPS, dtype=dtype)
    for run in range(runs):
        # Connect to SUMO simulation
        traci.start(
            ["sumo", "-c", path.abspath(inputFile), "--seed", str(SEED), "--emission-output", "emissions.xml"])

        # simulation loop
        step = 0
        while step < SCHEDULE_MAX_STEPS:
            traci.simulationStep()

            persons = traci.person.getIDList()

            pedestrianCount = len(persons)
            averageWaitTime = getAverageWaitTime(persons)
            averagePeopleAtBusStops = getAveragePeopleAtBusStops()

            if run == 0:
                data['Step'][step] = step
            data['AveragePeopleAtBusStops'][step] += averagePeopleAtBusStops
            data['AverageWaitTime'][step] += averageWaitTime

            step += 1
        traci.close()
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs
    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    if (path.isdir("../Output") == False):
        mkdir("../Output")
    np.savetxt(f"../Output/{outputFileName}", data, delimiter=',',
               fmt='%f', header="Step,AveragePeopleAtBusStops,AverageWaitTime")
    return data


if __name__ == "__main__":
    data = ScheduleVersion()
    PlotBoth(data)
