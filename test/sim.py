import traci
import pytz
import datetime

# Connect to SUMO simulation
traci.start(["sumo", "-c", "C:\\Users\\sebas\\Sumo\\test\\test.sumocfg"])

def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("Europe/Copenhagen"))
        DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        return DATIME

packBigData = []

# Simulation loop
step = 0
while step < 1000:
    traci.simulationStep()

    vehicles=traci.vehicle.getIDList()
    trafficlights=traci.trafficlight.getIDList()
    # Your simulation logic here
    step += 1
    
    for i in range(0,len(vehicles)):

            #Function descriptions
            #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
            #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
            vehicleId = vehicles[i]
            vehicleSpeed = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
            capacity = traci.vehicle.getPersonCapacity(vehicles[i])
            vehList = [getdatetime(), vehicleId, vehicleSpeed, capacity]

            idd = traci.vehicle.getLaneID(vehicles[i])
            packBigData.append(vehList)         

            # ML code/funcs here
            print(vehList)

            # control vehicles 

traci.close() 