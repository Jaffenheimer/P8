using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using p8mobility.persistence.UserRepository;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private static StateController.StateController _stateController;
    private readonly IUserRepository _userRepository;

    public AdminController(IBusStopRepository busStopRepository, IUserRepository userRepository,
        IBusRepository busRepository, IRouteRelationsRepository routeRelationsRepository)
    {
        _busStopRepository = busStopRepository;
        _userRepository = userRepository;
        _busRepository = busRepository;
        _routeRelationsRepository = routeRelationsRepository;
        _stateController =
            new StateController.StateController(_busStopRepository, _busRepository, _routeRelationsRepository);
        _stateController.Init();
        _stateController.Run();
    }

    /// <summary>
    /// Create a user
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if successful with the user object, otherwise bad request</returns>
    [HttpPost("createUser")]
    public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest req)
    {
        await _userRepository.CreateUser(Guid.NewGuid(), req.Username, req.Password);
        var res = await _userRepository.GetUser(req.Username);
        if(res == null)
            return BadRequest("User could not be created");
        return Ok(res);
    }
    
    [HttpPost("createBusStop")]
    public async Task<IActionResult> CreateBusStop([FromBody] CreateBusStopRequest req)
    {
        var res = await _busStopRepository.UpsertBusStop(Guid.NewGuid(), req.Latitude, req.Longitude);
        if (!res) return BadRequest("Could not create bus stop");
        return Ok("Bus stop created succesfully");
    }
    
    [HttpPost("createRoute")]
    public async Task<IActionResult> CreateRoute([FromBody] CreateRouteRequest req)
    {
        var res = await _routeRelationsRepository.UpsertRoute(Guid.NewGuid(), req.Name);
        if (!res) return BadRequest("Could not create route");
        return Ok("Route created succesfully");
    }
    
    [HttpPost("createRouteRelation")]
    public async Task<IActionResult> CreateRouteRelation([FromBody] CreateRouteRelationRequest req)
    {
        var res = await _routeRelationsRepository.UpsertRouteRelation(req.RouteId, req.BusStopId);
        if (!res) return BadRequest("Could not create route relation");
        return Ok("Route relation created succesfully");
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest req)
    {
        var res = await _userRepository.LogIn(req.Username, req.Password);
        var bus = new Bus(req.Latitude, req.Longitude, res.Id);
        bus.Country = req.Country;
        _stateController.AddBus(bus);
        return Ok(res);
    }

    [HttpPost("bus/location")]
    public async Task<IActionResult> UpdateBusLocation(decimal latitude, decimal longitude, Guid busId)
    {
        _stateController.UpdateBusLocation(busId, latitude, longitude);
        return Ok($"Bus with id {busId} was updated to location: {latitude}, {longitude}");
    }

    [HttpGet("bus/action")]
    public Task<IActionResult> BusAction(Guid id)
    {
        var res = _stateController.GetBus(id);
        return Task.FromResult<IActionResult>(Ok(res));
    }

    //Maybe create a service to retrieve this.
    [HttpPost("people/amount")]
    public async Task<IActionResult> UpdatePeopleAmount(int amount, Guid busStopId)
    {
        await _busStopRepository.UpdatePeopleCount(busStopId, amount);
        _stateController.UpdatePeopleCount(busStopId, amount);
        return Ok($"Successfully updated people amount on bus stop with id: {busStopId} to {amount}");
    }

    [HttpGet("people/amount")]
    public async Task<IActionResult> GetPeopleAmount(Guid busStopId)
    {
        return Ok("Det virkede :D");
    }

    [HttpDelete("shutdown/bus")]
    public Task<IActionResult> DeleteBus(Guid id)
    {
        _stateController.DeleteBus(id);
        return Task.FromResult<IActionResult>(Ok($"Bus with id {id} was shut down"));
    }
}