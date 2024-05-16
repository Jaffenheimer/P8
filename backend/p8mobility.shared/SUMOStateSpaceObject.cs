using System;
using System.Collections.Generic;

namespace p8_shared;

public class SUMOStateSpaceObject
{
    public List<double> AverageWaitTime { get; set; }
    public List<double> AveragePeopleAtBusStops { get; set; }
    public List<List<DummyBus>> Buses { get; set; } 
    
    public SUMOStateSpaceObject(List<double> averageWaitTime, List<double> averagePeopleAtBusStops, List<List<DummyBus>> buses)
    {
        AverageWaitTime = averageWaitTime;
        AveragePeopleAtBusStops = averagePeopleAtBusStops;
        Buses = buses;
    }
}