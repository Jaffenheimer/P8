using System.Collections.Generic;

namespace p8_shared;

public class State
{
    public List<Route> Routes { get; set; }
    public IEnumerable<Bus> Buses { get; set; }

    public State(IEnumerable<Bus> buses, List<Route> routes)
    {
        Buses = buses;
        Routes = routes;
    }
}