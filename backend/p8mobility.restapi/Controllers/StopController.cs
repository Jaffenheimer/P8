using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace p8_restapi.Controllers;

[ApiController]
[Route("stops")]
public class StopController : ControllerBase
{
    public StopController()
    {
    }

    [HttpPost("GetPeopleCount")]
    public async Task<IActionResult> FetchPeopleCount()
    {
        return Ok("Okidoki");
    }
}
