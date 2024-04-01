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
[Route("bus")]
public class BusController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private static StateController.StateController _stateController;
    private readonly IUserRepository _userRepository;

    public BusController(IBusStopRepository busStopRepository,
        IBusRepository busRepository, IRouteRelationsRepository routeRelationsRepository)
    {
        _busStopRepository = busStopRepository;
        _busRepository = busRepository;
        _routeRelationsRepository = routeRelationsRepository;
        _stateController =
            new StateController.StateController(_busStopRepository, _busRepository, _routeRelationsRepository);
        _stateController.Init();
        _stateController.Run();
    }
    
    
    [HttpPost("location")]
    public async Task<IActionResult> UpdateBusLocation(decimal latitude, decimal longitude, Guid busId)
    {
        _stateController.UpdateBusLocation(busId, latitude, longitude);
        return Ok($"Bus with id {busId} was updated to location: {latitude}, {longitude}");
    }

    [HttpGet("action")]
    public Task<IActionResult> BusAction(Guid id)
    {
        var res = _stateController.GetBus(id);
        return Task.FromResult<IActionResult>(Ok(res));
    }
    [HttpDelete("shutdown")]
    public Task<IActionResult> DeleteBus(Guid id)
    {
        _stateController.DeleteBus(id);
        return Task.FromResult<IActionResult>(Ok($"Bus with id {id} was shut down"));
    }

}