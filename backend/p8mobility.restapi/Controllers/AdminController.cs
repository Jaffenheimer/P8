using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_shared;
using p8mobility.persistence.BusStopRepository;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase{
    private readonly IBusStopRepository _busStopRepository;
    private static StateController.StateController _stateController;
    public AdminController(IBusStopRepository busStopRepository)
    {
        _busStopRepository = busStopRepository;
        _stateController = new StateController.StateController(_busStopRepository, new List<Bus>(), new List<BusStop>());
        _stateController.Init();
        _stateController.Run();
    }
    
    [HttpPost("createuser")]
    public async Task<IActionResult> CreateUser()
    {
        return Ok("Det virkede :D");
    }
    [HttpPost("login")]
    public async Task<IActionResult> Login()
    {
        return Ok("Det virkede :D");
    }
    
    [HttpPost("initiate/Bus")]
    public async Task<IActionResult> InitiateBus(decimal latitude, decimal longitude, Guid busId)
    {
        _stateController.AddBus(new Bus(latitude,longitude,busId));
        return Ok("Det virkede :D");
    }
    [HttpPost("bus/location")]
    public async Task<IActionResult> UpdateBusLocation(decimal latitude, decimal longitude, Guid busId)
    {
        return Ok("Det virkede :D");
    }
    
    [HttpGet("bus/action")]
    public async Task<IActionResult> BusAction(Guid id)
    {
        return Ok("Det virkede :D");
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
    
    
    
    
    
    
    
}