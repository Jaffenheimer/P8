using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using p8_restapi.PusherService;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using Action = p8_shared.Action;

namespace p8_restapi.StateController;

public class StateController
{
    private State SystemState { get; set; } = new State(new List<Bus>(), new List<Route>());
    private List<Route> Routes { get; set; }
    private bool Running { get; set; } = true;
    private List<BusStop> BusStops { get; set; }

    public async void Init(IBusStopRepository busStopRepository, IRouteRelationsRepository routeRelationsRepository, IBusRepository busRepository)
    {
        BusStops = await busStopRepository.GetAllBusStops();
        var routeIds = await routeRelationsRepository.GetRouteIds();
        foreach (var routeId in routeIds)
        {
            var busStopIds = await routeRelationsRepository.GetBusStopIdsFromRouteId(routeId);
            var route = new Route(routeId, BusStops.FindAll(busStop => busStopIds.Contains(busStop.Id)));
            Routes.Add(route);
        }

        var buses = await busRepository.GetAllBuses();
        SystemState = new State(buses, Routes);
    }

    public void Run(IPusherService pusherService)
    {
        while (Running)
        {
            //Maybe look into making a better solution
            //Task.Delay(2000);


            //Mutex might be necessary
            var currentState = SystemState;
            SystemState = UpdateState(currentState);
            var pusherMessage = new PusherMessage(new Dictionary<Guid, Action>());
            foreach (var state in SystemState.Buses)
            {
                pusherMessage.Actions.Add(state.Id, state.Action);
            }
            pusherService.PublishAction("state", "update", pusherMessage);
        }
    }

    public async void UpdateBusLocation(Guid id, decimal latitude, decimal longitude, IBusRepository busRepository)
    {
        var bus = GetBus(id);
        bus.Latitude = latitude;
        bus.Longitude = longitude;
        await busRepository.UpdateBusLocation(id, latitude, longitude);
    }

    public async void UpdateBusAction(Guid id, Action action, IBusRepository busRepository)
    {
        var bus = GetBus(id);
        bus.Action = action;
        await busRepository.UpdateBusAction(id, action);
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
        Console.WriteLine("Bus added");
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

    public void Restart(IBusStopRepository busStopRepository, IBusRepository busRepository,IRouteRelationsRepository routeRelationsRepository,PusherService.PusherService pusherService)
    {
        Running = true;
        Init(busStopRepository, routeRelationsRepository, busRepository);
        Run(pusherService);
    }

    public void Stop()
    {
        Running = false;
    }
}