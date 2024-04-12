using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using p8_restapi.PusherService;
using p8_restapi.Requests;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using Action = p8_shared.Action;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private readonly IPusherService _pusherService;
    
    public AdminController(IBusStopRepository busStopRepository,
        IBusRepository busRepository, IRouteRelationsRepository routeRelationsRepository, IPusherService pusherService)
    {
        _busStopRepository = busStopRepository;
        _busRepository = busRepository;
        _routeRelationsRepository = routeRelationsRepository;
        _pusherService = pusherService;
    }
    
    [HttpPost("initProgram")]
    public async Task<IActionResult> InitProgram()
    {
        if(Program._stateController.IsRunning){
            return BadRequest("Program already initialized");
        }
        await Program._stateController.Init(_busStopRepository, _routeRelationsRepository);
        // create a new thread to run the pusher service
        new Thread(() => Program._stateController.Run(_pusherService)).Start();
        return Ok("Program initialized");
    }
    
    /// <summary>
    /// Creates an Instance of a bus in the system
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if successful otherwise bad request</returns>
    [HttpPost("bus")]
    public async Task<IActionResult> CreateBus([FromBody] CreateBusRequest req)
    {
        var routeId = await _routeRelationsRepository.GetRouteFromPassword(req.Password);
        if (routeId == Guid.Empty || routeId == null) 
            return BadRequest("Could not log in");
        var bus = new Bus(req.Latitude, req.Longitude, Guid.NewGuid(), routeId.Value);
        var res = await _busRepository.Upsert(bus.Id, routeId.Value, bus.Latitude, bus.Longitude, Action.Default);
        if (!res)
            return BadRequest("Could not log in");
        Program._stateController.AddBus(bus);
        return Ok(bus.Id);
    }
    
    /// <summary>
    /// Creates a bus stop
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if bus stop is created otherwise bad request</returns>
    [HttpPost("busStop")]
    public async Task<IActionResult> CreateBusStop([FromBody] CreateBusStopRequest req)
    {
        var res = await _busStopRepository.UpsertBusStop(Guid.NewGuid(), req.Latitude, req.Longitude);
        if (!res) 
            return BadRequest("Could not create bus stop");
        
        return Ok("Bus stop created succesfully");
    }
    
    /// <summary>
    /// Creates a bus route
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if bus route is created otherwise bad request</returns>
    [HttpPost("route")]
    public async Task<IActionResult> CreateRoute([FromBody] CreateRouteRequest req)
    {
        var res = await _routeRelationsRepository.UpsertRoute(Guid.NewGuid(), req.Password, req.BusStopIds);
        if (!res) 
            return BadRequest("Could not create route");
        
        return Ok("Route created succesfully");
    }
    
    /// <summary>
    /// Updates bus to be at a new location
    /// </summary>
    /// <param name="latitude"></param>
    /// <param name="longitude"></param>
    /// <param name="busId"></param>
    /// <returns>Ok with confirmation of where bus is</returns>
    [HttpPost("bus/location")]
    public async Task<IActionResult> UpdateBusLocation(decimal latitude, decimal longitude, Guid busId)
    {
        Program._stateController.UpdateBusLocation(busId, latitude, longitude,_busRepository);
        return Ok($"Bus with id {busId} was updated to location: {latitude}, {longitude}");
    }

    /// <summary>
    /// Retrieves the calculated action for a specific bus
    /// </summary>
    /// <param name="id"></param>
    /// <returns>Action</returns>
    [HttpGet("bus/action")]
    public Task<IActionResult> BusAction(Guid id)
    {
        var res = Program._stateController.GetBus(id);
        return Task.FromResult<IActionResult>(Ok(res));
    }

    /// <summary>
    /// Shutdown/Deletes bus
    /// </summary>
    /// <param name="id"></param>
    /// <returns>Ok with confirmation of where id of bus</returns>
    [HttpDelete("bus")]
    public async Task<IActionResult> DeleteBus(Guid id)
    {
        Program._stateController.DeleteBus(id);

        if (await _busRepository.DeleteBus(id))
            return Ok($"Bus with id {id} was deleted");
        
        return BadRequest("Could not delete bus");
    }

    /// <summary>
    /// Updates the amount of people at a bus stop
    /// </summary>
    /// <param name="amount"></param>
    /// <param name="busStopId"></param>
    /// <returns>Ok with confirmation of what bus stop is updated with how many people</returns>
    [HttpPost("people/amount")]
    public async Task<IActionResult> UpdatePeopleAmount(int amount, Guid busStopId)
    {
        await _busStopRepository.UpdatePeopleCount(busStopId, amount);
        Program._stateController.UpdatePeopleCount(busStopId, amount);
        return Ok($"Successfully updated people amount on bus stop with id: {busStopId} to {amount}");
    }
    
}