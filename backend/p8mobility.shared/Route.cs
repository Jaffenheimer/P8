using System;
using System.Collections.Generic;

namespace p8_shared;

public class Route
{
    public Guid Id { get; set; }
    public List<BusStop> BusStops { get; set; }

    public Route()
    {
    }

    public Route(Guid id, List<BusStop> busStops)
    {
        Id = id;
        BusStops = busStops;
    }
}