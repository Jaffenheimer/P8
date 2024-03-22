using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
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
            //Maybe look into making a better solution
            Task.Delay(2000);
            
            
            //Mutex might be necessary
            var mutex = new Mutex();
            var currentState = SystemState;
            SystemState = UpdateState(currentState);
            mutex.ReleaseMutex();
        }
    }
    
    public void UpdateBusLocation(Guid id, decimal latitude, decimal longitude)
    {
        var bus = GetBus(id);
        bus.Latitude = latitude;
        bus.Longitude = longitude;
    }

    public State GetState()
    {
        return SystemState;
    }
    
    public Bus GetBus(Guid id)
    {
        var res = SystemState.Buses.Find(bus => bus.Id == id);
        
        return res ?? throw new Exception("Bus not found");
    }
    
    public void AddBus(Bus bus)
    {
        SystemState.Buses.Add(bus);
    }
    
    public void DeleteBus(Guid id)
    {
        var bus = GetBus(id); 
        SystemState.Buses.Remove(bus);
    }

    private State UpdateState(State currentState)
    {
        //Compute new state
        return new State(new List<Bus>(), new List<BusStop>());
    }
    
    public void Restart()
    {
        Running = true;
        Init();
        Run();
    }

    public void Stop()
    {
        Running = false;
    }
}