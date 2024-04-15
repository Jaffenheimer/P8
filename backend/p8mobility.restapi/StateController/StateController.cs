using System;
using System.Collections.Generic;
using System.Linq;
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
    private static State SystemState { get; set; }
    private static List<Route> Routes { get; set; } = new List<Route>();
    public static bool Running { get; set; } = true;
    public bool IsRunning { get; set; } = false;
    private static List<BusStop> BusStops { get; set; } = new List<BusStop>();

    public async Task Init(IBusStopRepository busStopRepository, IRouteRelationsRepository routeRelationsRepository)
    {
        BusStops = await busStopRepository.GetAllBusStops();
        var routeIds = await routeRelationsRepository.GetRouteIds();
        foreach (var routeId in routeIds)
        {
            var busStopIds = await routeRelationsRepository.GetBusStopIdsFromRouteId(routeId);
            var route = new Route(routeId, BusStops.FindAll(busStop => busStopIds.Contains(busStop.Id)));
            Routes.Add(route);
        }

        SystemState = new State(new List<Bus>(), Routes);
        Console.WriteLine("StateController initialized");
    }

    public void Run(IPusherService pusherService)
    {
        IsRunning = true;
        Console.WriteLine("Running");
        while (Running)
        {
            //Maybe look into making a better solution
            //Task.Delay(2000);


            //Mutex might be necessary
            var currentState = SystemState;
            //SystemState = UpdateState(currentState);
            var pusherMessage = new PusherMessage(new Dictionary<Guid, Action>());
            if (SystemState.Buses.Any() && currentState.Buses.Any())
            {
                foreach (var bus in SystemState.Buses.ToList())
                {
                    if (bus.Action != currentState.Buses.ToList().Find(bus2 => bus2.Id == bus.Id)!.Action)
                    {
                        pusherMessage.Actions.Add(bus.Id, bus.Action);
                    }
                }
            }


            //Currently we dont want to publish anything
            if (pusherMessage.Actions.Count > 0)
            {
                //pusherService.PublishAction("action", "update", pusherMessage);
            }

            pusherMessage.Actions.Clear();
        }

        IsRunning = false;
    }

    public async Task<bool> UpdateBusLocation(Guid id, decimal latitude, decimal longitude, IBusRepository busRepository)
    {
        var bus = GetBus(id);
        if (bus == null)
            return false;
        bus.Latitude = latitude;
        bus.Longitude = longitude;
        await busRepository.UpdateBusLocation(id, latitude, longitude);
        Console.WriteLine("Bus location updated");
        return true;
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

    public Bus? GetBus(Guid id)
    {
        var res = SystemState.Buses.ToList().Find(bus => bus.Id == id);

        if (res == null)
            return null;

        return res;
    }

    public void AddBus(Bus bus)
    {
        lock (SystemState.Buses)
        {
            SystemState.Buses = SystemState.Buses.Append(bus);
        }

        Console.WriteLine("Bus added");
    }

    public void DeleteBus(Guid id)
    {
        var bus = GetBus(id);
        SystemState.Buses.ToList().Remove(bus);
        if (!SystemState.Buses.Any())
        {
            SystemState.Buses = new List<Bus>();
        }

        Console.WriteLine("Bus deleted");
    }

    private State UpdateState(State currentState)
    {
        //Compute new state
        return new State(new List<Bus>(), new List<Route>());
    }

    public async void Restart(IBusStopRepository busStopRepository, IBusRepository busRepository,
        IRouteRelationsRepository routeRelationsRepository, PusherService.PusherService pusherService)
    {
        Running = true;
        await Init(busStopRepository, routeRelationsRepository);
        Run(pusherService);
    }

    public void Stop()
    {
        Running = false;
    }
}