import traci


def average_people_at_busstops():
    busstops = traci.busstop.getIDList()
    people_at_busstops = []
    for busstop in busstops:
        people_at_busstops.append(traci.busstop.getPersonCount(busstop))
    # Calculate average
    return sum(people_at_busstops) / len(people_at_busstops)
