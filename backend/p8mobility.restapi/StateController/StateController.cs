using System.Collections.Generic;
using p8_shared;
using p8mobility.persistence.BusStopRepository;

namespace p8_restapi.StateController;

public class StateController
{
    private readonly IBusStopRepository _busStopRepository;
    private State SystemState { get; set; }
    private bool Running { get; set; } = true;
    
    public StateController(IBusStopRepository busStopRepository, List<Bus> buses, List<BusStop> busStops)
    {
        _busStopRepository = busStopRepository;
        SystemState = new State(buses, busStops);
    }
    
    public async void Init()
    {
        var buses = new List<Bus>();
        var busStops = await _busStopRepository.GetAllBusStops();
        SystemState = new State(buses, busStops);
    }

    public void Run()
    {
        while (Running)
        {
            var currentState = SystemState;
            SystemState = UpdateState(currentState);
        }
    }

    public State GetState()
    {
        return SystemState;
    }
    public void AddBus(Bus bus)
    {
        SystemState.Buses.Add(bus);
    }

    private State UpdateState(State? currentState)
    {
        //Compute new state
        return new State(new List<Bus>(), new List<BusStop>());
    }

    public void Stop()
    {
        Running = false;
    }
}