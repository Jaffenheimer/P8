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

    [HttpPost("FetchPeopleCountFromClient")]
    public async Task<IActionResult> FetchPeopleCount([FromBody] StopRequest req)
    {   
        return Ok("PeopleCount: " + req.PeopleCount);
    }

    [HttpGet("GetPeopleCountFromId")]
    public async Task<IActionResult> GetPeopleCountFromId([FromQuery] StopRequest req)
    {
        var res = await _busStopRepository.GetPeopleCountFromId(req.Id);
        if (res is null) return BadRequest("Bus stop not found");
        return Ok(res.PeopleCount);
    }

    [HttpPut("CreateBusStop")]
    public async Task<IActionResult> CreateBusStop([FromQuery] StopRequest req)
    {
        var res = await _busStopRepository.UpsertBusStop(req.Id, req.Latitude, req.Longitude, req.PeopleCount);
        if (!res) return BadRequest("Could not create bus stop");
        return Ok("Bus stop created succesfully");
    }

    [HttpPatch("UpdatePeopleCount")]
    public async Task<IActionResult> UpdatePeopleCount([FromBody] StopRequest req)
    {
        var res = await _busStopRepository.ChangePeopleCount(req.Id, req.PeopleCount);
        if (!res) return BadRequest("PeopleCount could not be updated");
        return Ok($"[{req.Id}] PeopleCount updated");
    }

    [HttpDelete("DeleteBusStop")]
    public async Task<IActionResult> DeleteBusStop([FromBody] StopRequest req)
    {
        var res = await _busStopRepository.DeleteBusStop(req.Id);
        if (!res) return BadRequest("Bus stop could not be deleted");
        return Ok($"Bus stop [{req.Id}] succesfully deleted");
    }

}