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
        //_stateController =
            //new StateController.StateController(_busStopRepository, _busRepository, _routeRelationsRepository);
        //_stateController.Init();
        //_stateController.Run();
    }

    /// <summary>
    /// Create a user
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if successful with the user object, otherwise bad request</returns>
    //maybe create user and login should be in a user controller
    [HttpPost("createUser")]
    public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest req)
    {
        await _userRepository.CreateUser(Guid.NewGuid(), req.Username, req.Password);
        var res = await _userRepository.GetUser(req.Username);
        if(res == null)
            return BadRequest("User could not be created");
        return Ok(res);
    }
    
    /// <summary>
    /// Logs the user in
    /// </summary>
    /// <param name="req"></param>
    /// <returns>Ok if user is logged in otherwise bad request</returns>
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest req)
    {
        var res = await _userRepository.LogIn(req.Username, req.Password);
        var bus = new Bus(req.Latitude, req.Longitude, res.Id);
        bus.Country = req.Country;
        _stateController.AddBus(bus);
        return Ok(res);
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
}