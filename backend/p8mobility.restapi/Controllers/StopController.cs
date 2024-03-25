using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;
using p8mobility.persistence.BusStopRepository;
using System;
using System.Threading.Tasks;

namespace p8_restapi.Controllers;

[ApiController]
[Route("stops")]
public class StopController : ControllerBase
{
    private IBusStopRepository _busStopRepository;
    public StopController(IBusStopRepository busStopRepository)
    {
        _busStopRepository = busStopRepository;
    }

    [HttpPost("GetPeopleCount")]
    public async Task<IActionResult> GetPeopleCount([FromBody] StopRequest req)
    {
        await Console.Out.WriteLineAsync(req.PeopleCount.ToString());
        
        return Ok("PeopleCount: " + req.PeopleCount);
    }
    [HttpGet("CreateBusStop")]
    public async Task<IActionResult> CreateBusStop([FromQuery] StopRequest req)
    {
        var res = await _busStopRepository.UpsertBusStop(req.Id, req.Latitude, req.Longitude, req.PeopleCount);
        if (!res) return BadRequest("Could not create bus stop");
        return Ok("Bus stop created succesfully");
    }
}