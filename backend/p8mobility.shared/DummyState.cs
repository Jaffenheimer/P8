using System.Collections.Generic;

namespace p8_shared;

public class DummyState
{
    public double AverageWaitTime { get; set; }
    public double AveragePeopleAtBusStops { get; set; }
    public List<DummyBus> Busses { get; set; }
    
    public DummyState(double averageWaitTime, double averagePeopleAtBusStops, List<DummyBus> busses)
    {
        AverageWaitTime = averageWaitTime;
        AveragePeopleAtBusStops = averagePeopleAtBusStops;
        Busses = busses;
    }
}