using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using p8_restapi.Requests;

namespace p8_restapi.Controllers;

[ApiController]
[Route("stops")]
public class StopController : ControllerBase
{
    public StopController()
    {
    }

    [HttpPost("GetPeopleCount")]
    public async Task<IActionResult> FetchPeopleCount([FromBody] StopRequest req)
    {
        await Console.Out.WriteLineAsync(req.PeopleCount.ToString());
        return Ok("PeopleCount: " + req.PeopleCount);
    }
}