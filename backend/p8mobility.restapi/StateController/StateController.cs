using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.Extensions.Primitives;
using p8_restapi.PusherService;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using static Org.BouncyCastle.Math.Primes;
using Action = p8_shared.Action;

namespace p8_restapi.StateController;

public class StateController
{
    public Dictionary<int, Guid> DummyBusIds = new Dictionary<int, Guid>()
    {
        {0, Guid.Parse("32ef5fd5-bd8f-49f3-98a9-c051c898b337")},
        {1, Guid.Parse("9ad3dda7-ee23-42e3-ba23-9ffd41fbc950")},
        {2, Guid.Parse("3582dfc5-8fce-48a5-b20d-8bcc128b0614")},
        {3, Guid.Parse("998b7ecb-d27c-41cb-9fdf-f376e03902b8")},
        {4, Guid.Parse("885b236c-449b-4f5f-be9f-14dc679b0b55")},
        {5, Guid.Parse("4a5c0375-153e-4f4c-8045-925938862d74")},
        {6, Guid.Parse("344412d3-0010-4f1d-aef8-8e1e8e7625c2")},
        {7, Guid.Parse("1f93239c-6f4f-4238-b0df-0532a939672a")},
        {8, Guid.Parse("fc491324-db22-448d-a487-4ace6e3f34a1")},
        {9, Guid.Parse("b957cc45-07ed-4d9b-8211-fe1343c0ed32")}
    };

    public int BussesInitialized = 0;

    private static State SystemState { get; set; }
    private static List<Route> Routes { get; set; } = new List<Route>();
    public static bool Running { get; set; } = true;
    public bool IsRunning { get; set; } = false;
    private static List<BusStop> BusStops { get; set; } = new List<BusStop>();
    private static Dictionary<Guid, Action> actions;

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

    public async void Run(IPusherService pusherService)
    {
        var sumoStateSpaceObject = HelperFunctions.ReadCsv();
        
        IsRunning = true;
        Console.WriteLine("Running");

        StringBuilder stb = new StringBuilder();
        
        for (int i = 0; i < sumoStateSpaceObject.StateCount; i++)
        {
            stb.Clear();
            DummyState dummyState = new DummyState(sumoStateSpaceObject.AverageWaitTime[i],
                sumoStateSpaceObject.AveragePeopleAtBusStops[i], sumoStateSpaceObject.Buses[i]);
            var j = 0;
            foreach (var bus in dummyState.Busses)
            {
                j++;
                stb.Append(bus.Position.ToString("F",
                  CultureInfo.InvariantCulture));
                stb.Append(',');
                stb.Append(bus.Speed.ToString("F",
                  CultureInfo.InvariantCulture));
                if (j != 10) 
                    stb.Append(',');
            }

            var p = new Process();
            p.StartInfo.FileName = "python.exe";

            //Feed dummy state to model
            p.StartInfo.Arguments = $"MiModel/TRPO.py {dummyState.AverageWaitTime.ToString("G",
                  CultureInfo.InvariantCulture)},{dummyState.AveragePeopleAtBusStops.ToString("G", CultureInfo.InvariantCulture)},{stb}";
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();

            //retrieve actions from model
            var actionString = await p.StandardOutput.ReadToEndAsync();
            var trimString = Regex.Replace(actionString, @"r[^\d.-]+", "").Trim().TrimStart('[').TrimEnd(']');
            var actionStringArray = trimString.Split(' ').Where(s => s != string.Empty).ToArray();
            var actionDoubleArray = Array.ConvertAll(actionStringArray, new Converter<string, double>(double.Parse));
            p.WaitForExit();
            FindActionStrings(out actions, actionDoubleArray);
            foreach (var kvp in actions)
            {
                await Console.Out.WriteLineAsync($"Id: {kvp.Key} | Action: {kvp.Value}");
            }

        }
        
        await Task.Delay(5000);            
            
        //Only used for real Life Application not for simulation
        //var currentState = SystemState;
        //SystemState = UpdateState(currentState);


        var pusherMessage = new PusherMessage(actions);

        var secondCounter = 0;

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

    }
    private void FindActionStrings(out Dictionary<Guid, Action> actions, double[] actionDoubleArray)
    {
        actions = new Dictionary<Guid, Action>(); //State No., action array
        var c = 0;
        foreach (var ad in actionDoubleArray)
        {
            switch (ad)
            {
                case <= -0.33:
                    actions.Add(DummyBusIds[c], Action.Decelerate);
                    break;
                case >= 0.33: actions.Add(DummyBusIds[c], Action.Accelerate);
                    break;
                default:
                    actions.Add(DummyBusIds[c], Action.MaintainSpeed);
                    break;
            }
            c++; //;)
        }
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