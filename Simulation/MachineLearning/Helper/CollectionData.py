import traci


def average_people_at_busstops():
    busstops = traci.busstop.getIDList()
    people_at_busstops = []
    for busstop in busstops:
        people_at_busstops.append(traci.busstop.getPersonCount(busstop))

    if len(people_at_busstops) == 0:
        return 0

    if sum(people_at_busstops) == 0:
        return 0

    return sum(people_at_busstops) / len(people_at_busstops)


def get_people_at_bus_stops():
    bus_stops = traci.busstop.getIDList()
    people_at_bus_stops = []

    for busstop in bus_stops:
        people_at_bus_stops.append(traci.busstop.getPersonCount(busstop))

    return people_at_bus_stops
