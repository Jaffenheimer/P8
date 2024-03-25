import traci
import pandas as pd

# Connect to SUMO simulation
traci.start(["sumo", "-c", "C:\\Users\\sebas\\Sumo\\test\\test.sumocfg"])

df = pd.DataFrame(
    {
    "Step": [],
    "Id": [],
    "Speed": [],
    "Capacity": []
    })

df2 = pd.DataFrame(
    {
    "Step": [],
    "Id": [],
    "Position": [],
    "Status": [],
    "WaitingTime": []
    })

step = 0
while step < 1000:
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()
    persons = traci.person.getIDList()

    step += 1
    
    #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
    #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
    for i in range(0,len(vehicles)):
        vehicleId = vehicles[i]
        vehicleSpeed = round(traci.vehicle.getSpeed(vehicleId)*3.6, 2) # m/s to km/h
        capacity = traci.vehicle.getPersonCapacity(vehicleId)
        df.loc[len(df)] = {"Step": step, "Id": vehicleId, "Speed": vehicleSpeed, "Capacity": capacity}
        
    #https://sumo.dlr.de/pydoc/traci._person.html
    for j in range(0,len(persons)):
        personId = persons[j]
        personPosition = traci.person.getPosition(personId)
        personStatus = traci.person.getStage(personId).type
        personWaitingTime = traci.person.getWaitingTime(personId)
        df2.loc[len(df2)] = {"Step": step, "Id": personId, "Position": str(personPosition), "Status": personStatus, "WaitingTime": personWaitingTime}

    # ML code/funcs here
    # control vehicles 

print()
print("---- VEHICLES ----")
print(df)

print("---- PERSONS ----")
print(df2)
traci.close() 
