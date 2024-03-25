using System.Collections.Generic;

namespace p8_shared;

public class State
{
    public List<Route> Routes { get; set; }
    public List<Bus> Buses { get; set; }

    public State(List<Bus> buses, List<Route> routes)
    {
        Buses = buses;
        Routes = routes;
    }
}