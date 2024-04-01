using System;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;
using p8mobility.persistence.BusStopRepository;
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;

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

}