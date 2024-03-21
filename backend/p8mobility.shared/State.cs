using System.Collections.Generic;

namespace p8_shared;

public class State
{
    public List<BusStop> BusStops { get; set; }
    public List<Bus> Buses { get; set; }

    public State(List<Bus> buses, List<BusStop> busStops)
    {
        Buses = buses;
        BusStops = busStops;
    }
}