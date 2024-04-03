using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private static StateController.StateController _stateController;

    public AdminController(IBusStopRepository busStopRepository,
        IBusRepository busRepository, IRouteRelationsRepository routeRelationsRepository)
    {
        _busStopRepository = busStopRepository;
        _busRepository = busRepository;
        _routeRelationsRepository = routeRelationsRepository;
        _stateController =
            new StateController.StateController(_busStopRepository, _busRepository, _routeRelationsRepository);
        _stateController.Init();
        var ts = new ThreadStart(_stateController.Run);
        var backgroundThread = new Thread(ts);
        backgroundThread.Start();
    }
    
    
    /// <summary>
    /// Logs the user in
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if user is logged in otherwise bad request</returns>
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest req)
    {
        return Ok("good shit");
    }
    
    /// <summary>
    /// Creates a bus stop
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if bus stop is created otherwise bad request</returns>
    [HttpPost("createBusStop")]
    public async Task<IActionResult> CreateBusStop([FromBody] CreateBusStopRequest req)
    {
        var res = await _busStopRepository.UpsertBusStop(Guid.NewGuid(), req.Latitude, req.Longitude);
        if (!res) return BadRequest("Could not create bus stop");
        return Ok("Bus stop created succesfully");
    }
    
    /// <summary>
    /// Creates a bus route
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if bus route is created otherwise bad request</returns>
    [HttpPost("createRoute")]
    public async Task<IActionResult> CreateRoute([FromBody] CreateRouteRequest req)
    {
        var res = await _routeRelationsRepository.UpsertRoute(Guid.NewGuid(), req.Name);
        if (!res) return BadRequest("Could not create route");
        return Ok("Route created succesfully");
    }
    
    /// <summary>
    /// Creates a route relation, that is connecting a bus stop to a route
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if route relation is created otherwise bad request</returns>
    [HttpPost("createRouteRelation")]
    public async Task<IActionResult> CreateRouteRelation([FromBody] CreateRouteRelationRequest req)
    {
        var res = await _routeRelationsRepository.UpsertRouteRelation(req.RouteId, req.BusStopId);
        if (!res) return BadRequest("Could not create route relation");
        return Ok("Route relation created succesfully");
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
        _stateController.UpdateBusLocation(busId, latitude, longitude);
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
        var res = _stateController.GetBus(id);
        return Task.FromResult<IActionResult>(Ok(res));
    }
    
    /// <summary>
    /// Shutdown/Deletes bus
    /// </summary>
    /// <param name="id"></param>
    /// <returns>Ok with confirmation of where id of bus</returns>
    [HttpDelete("bus/shutdown")]
    public Task<IActionResult> DeleteBus(Guid id)
    {
        _stateController.DeleteBus(id);
        return Task.FromResult<IActionResult>(Ok($"Bus with id {id} was shut down"));
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
        _stateController.UpdatePeopleCount(busStopId, amount);
        return Ok($"Successfully updated people amount on bus stop with id: {busStopId} to {amount}");
    }

    /// <summary>
    /// Gets the amount of people at a bus stop
    /// </summary>
    /// <param name="busStopId"></param>
    /// <returns>Ok</returns>
    [HttpGet("people/amount")]
    public async Task<IActionResult> GetPeopleAmount(Guid busStopId)
    {
        return Ok("Det virkede :D");
    }
    
}