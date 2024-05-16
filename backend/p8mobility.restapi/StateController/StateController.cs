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
    public Dictionary<string, Guid> DummyBusIds = new Dictionary<string, Guid>()
    {
        {"bus_r_0_0", Guid.Parse("32ef5fd5-bd8f-49f3-98a9-c051c898b337")},
        {"bus_r_1_0", Guid.Parse("9ad3dda7-ee23-42e3-ba23-9ffd41fbc950")},
        {"bus_r_0_1", Guid.Parse("3582dfc5-8fce-48a5-b20d-8bcc128b0614")},
        {"bus_r_1_1", Guid.Parse("998b7ecb-d27c-41cb-9fdf-f376e03902b8")},
        {"bus_r_0_2", Guid.Parse("885b236c-449b-4f5f-be9f-14dc679b0b55")},
        {"bus_r_1_2", Guid.Parse("4a5c0375-153e-4f4c-8045-925938862d74")},
        {"bus_r_0_3", Guid.Parse("344412d3-0010-4f1d-aef8-8e1e8e7625c2")},
        {"bus_r_1_3", Guid.Parse("1f93239c-6f4f-4238-b0df-0532a939672a")},
        {"bus_r_0_4", Guid.Parse("fc491324-db22-448d-a487-4ace6e3f34a1")},
        {"bus_r_1_4", Guid.Parse("b957cc45-07ed-4d9b-8211-fe1343c0ed32")}
    };

    public int BussesInitialized = 0;

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
        var sumoStateSpaceObject = HelperFunctions.ReadCsv();
        
        IsRunning = true;
        Console.WriteLine("Running");
        
        int counter = 0;
        while (Running)
        {
            DummyState dummyState = new DummyState(sumoStateSpaceObject.AverageWaitTime[counter],
                sumoStateSpaceObject.AveragePeopleAtBusStops[counter], sumoStateSpaceObject.Buses[counter]);
           
           
            Task.Delay(5000);
            
            //Feed dummy state to model
            //retrieve actions from model
            int[] actions = new int[9];
            
            
            //Only used for real Life Application not for simulation
            //var currentState = SystemState;
            //SystemState = UpdateState(currentState);


            var pusherMessage = new PusherMessage(new Dictionary<Guid, Action>());

            var secondCounter = 0;
            foreach (var bus in dummyState.Busses)
            {
                Action act = 0;
                
                if(actions[secondCounter] == 1)
                    act = Action.Accelerate;
                if(actions[secondCounter] == 0)
                    act = Action.MaintainSpeed;
                if(actions[secondCounter] == -1)
                    act = Action.Decelerate;
                
                pusherMessage.Actions.Add(bus.Id, act);
                secondCounter++;
            }
            //Only used for real Life Application not for simulation
            /*if (SystemState.Buses.Any() && currentState.Buses.Any())
            {
                var currentBuses = currentState.Buses.ToList();
                var systemBuses = SystemState.Buses.ToList();

                foreach (var bus in systemBuses)
                {
                    var currentBus = currentBuses.Find(bus2 => bus2.Id == bus.Id);
                    if (currentBus != null && bus.Action != currentBus.Action)
                    {
                        pusherMessage.Actions.Add(bus.Id, bus.Action);
                    }
                }
            }*/
            
            if (pusherMessage.Actions.Count > 0)
            {
                pusherService.PublishAction("action", "update", pusherMessage);
            }

            pusherMessage.Actions.Clear();
            counter++;
        }

        IsRunning = false;
    }

    public async Task<bool> UpdateBusLocation(Guid id, decimal latitude, decimal longitude,
        IBusRepository busRepository)
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