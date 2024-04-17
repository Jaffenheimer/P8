import traci
import pandas as pd
import numpy as np
from os import path, mkdir
from random import randint
import asyncio

def ScheduleVersion(inputFile="../SUMO/schedule/schedule.sumocfg", outputFileName="output_schedule.csv", steps=500):
    # initializations
    
    dtype = [('Step', int), ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)
    # Connect to SUMO simulation
    try:
        traci.close()
    except:
        pass
    traci.start(["sumo", "-c", path.abspath(inputFile),"--seed",str(randint(1,100000))])

    # simulation loop
    step = 0
    while step < steps:
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
    np.savetxt(f"../Output/{outputFileName}", data, delimiter=',',fmt='%f', header="Step,AveragePeopleAtBusStops,AverageWaitTime") 
    return data
  
     
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
    busStops = ["bs_road_-overlap","bs_road_-R2", "bs_road_-R1", "bs_road_-R0", "bs_road_-L3", "bs_road_-L2", "bs_road_-L1", "bs_road_-L0"] # excluding overlap for special case handling
    
    totalPeopleAtBusStops = 0
    ### finds the number of people at each bus stop
    for busStop in busStops:
        totalPeopleAtBusStops += traci.busstop.getPersonCount(busStop)
    return totalPeopleAtBusStops/len(busStops)
    
#now for multiple runs, where the values are the average of the runs:
def runMultiple(inputFile="../SUMO/algorithm/algorithm.sumocfg", outputFileName="output.csv", steps=500, shouldMakePlots=False, runs=10):
    dtype = [('Step', int), ('PedestrianCount', float), ('AveragePeopleAtBusStops', float), ('AverageWaitTime', float)]
    data = np.zeros(steps, dtype=dtype)
    for run in range(runs):
        # Connect to SUMO simulation
        traci.start(["sumo", "-c", path.abspath(inputFile),"--seed",str(randint(1,100000))])

        # simulation loop
        step = 0
        while step < steps:
            traci.simulationStep()
            
            persons = traci.person.getIDList()
            
            
            pedestrianCount = len(persons)
            averageWaitTime = getAverageWaitTime(persons)
            averagePeopleAtBusStops = getAveragePeopleAtBusStops()
            
            if run == 0:
                data['Step'][step] = step
            # if run == 800:
            #     print(data['PedestrianCount'][step])
            data['PedestrianCount'][step] += pedestrianCount
            data['AveragePeopleAtBusStops'][step] += averagePeopleAtBusStops
            data['AverageWaitTime'][step] += averageWaitTime
            # data.loc[len(data)] = {"Step": step, "PedestrianCount": pedestrianCount, "AveragePeopleAtBusStops": averagePeopleAtBusStops, "AverageWaitTime": averageWaitTime}
            
            step += 1
        traci.close()
        # print(run)
        # print(data['AverageWaitTime'][800])
    data['PedestrianCount'] = data['PedestrianCount']/runs
    data['AveragePeopleAtBusStops'] = data['AveragePeopleAtBusStops']/runs
    data['AverageWaitTime'] = data['AverageWaitTime']/runs
    if shouldMakePlots:
        makePlots(data)
    if (path.isdir("../Output") == False):
        mkdir("../Output")
    np.savetxt(f"../Output/{outputFileName}", data, delimiter=',',fmt='%f', header="Step,PedestrianCount,AveragePeopleAtBusStops,AverageWaitTime")