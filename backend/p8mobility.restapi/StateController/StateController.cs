using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using Action = p8_shared.Action;

namespace p8_restapi.StateController;

public class StateController
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private State SystemState { get; set; }
    private List<Route> Routes { get; set; }
    private bool Running { get; set; } = true;
    private List<BusStop> BusStops { get; set; }

    public StateController(IBusStopRepository busStopRepository, IBusRepository busRepository,
        IRouteRelationsRepository routeRelationsRepository)
    {
        _busStopRepository = busStopRepository;
        _busRepository = busRepository;
        _routeRelationsRepository = routeRelationsRepository;
    }

    public async void Init()
    {
        BusStops = await _busStopRepository.GetAllBusStops();
        var routeIds = await _routeRelationsRepository.GetRouteIds();
        foreach (var routeId in routeIds)
        {
            var busStopIds = await _routeRelationsRepository.GetBusStopIdsFromRouteId(routeId);
            var route = new Route(routeId, BusStops.FindAll(busStop => busStopIds.Contains(busStop.Id)));
            Routes.Add(route);
        }

        var buses = await _busRepository.GetAllBuses();
        SystemState = new State(buses, Routes);
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

    public void UpdateBusAction(Guid id, Action action)
    {
        var bus = GetBus(id);
        bus.Action = action;
    }

    public void UpdatePeopleCount(Guid busStopId, int peopleCount)
    {
        BusStops.Find(busStop => busStop.Id == busStopId)!.PeopleCount = peopleCount;
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
        return new State(new List<Bus>(), new List<Route>());
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