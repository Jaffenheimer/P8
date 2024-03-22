using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;
using p8_shared;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.UserRepository;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private static StateController.StateController _stateController;
    private readonly IUserRepository _userRepository;

    public AdminController(IBusStopRepository busStopRepository, IUserRepository userRepository)
    {
        _busStopRepository = busStopRepository;
        _userRepository = userRepository;
        _stateController =
            new StateController.StateController(_busStopRepository, new List<Bus>(), new List<BusStop>());
        _stateController.Init();
        _stateController.Run();
    }

    [HttpPost("createuser")]
    public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest req)
    {
        await _userRepository.CreateUser(Guid.NewGuid(), req.Username, req.Password);
        var res = await _userRepository.GetUser(req.Username);
        return Ok(res);
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest req)
    {
        var res = await _userRepository.LogIn(req.Username, req.Password);
        _stateController.AddBus(new Bus(req.Latitude, req.Longitude, res.Id));
        return Ok(res);
    }

    [HttpPost("bus/location")]
    public async Task<IActionResult> UpdateBusLocation(decimal latitude, decimal longitude, Guid busId)
    {
        _stateController.UpdateBusLocation(busId, latitude, longitude);
        return Ok("Det virkede :D");
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
        return Ok("Det virkede :D");
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