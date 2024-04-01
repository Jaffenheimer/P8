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
[Route("people")]
public class PeopleController : ControllerBase
{
    private readonly IBusStopRepository _busStopRepository;
    private readonly IBusRepository _busRepository;
    private readonly IRouteRelationsRepository _routeRelationsRepository;
    private static StateController.StateController _stateController;
    private readonly IUserRepository _userRepository;

    public PeopleController(IBusStopRepository busStopRepository,
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


    [HttpPost("amount")]
    public async Task<IActionResult> UpdatePeopleAmount(int amount, Guid busStopId)
    {
        await _busStopRepository.UpdatePeopleCount(busStopId, amount);
        _stateController.UpdatePeopleCount(busStopId, amount);
        return Ok($"Successfully updated people amount on bus stop with id: {busStopId} to {amount}");
    }

    [HttpGet("amount")]
    public async Task<IActionResult> GetPeopleAmount(Guid busStopId)
    {
        return Ok("Det virkede :D");
    }
}