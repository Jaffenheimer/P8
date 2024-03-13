using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace p8_restapi.Controllers;

[ApiController]
[Route("admin")]
public class AdminController : ControllerBase{
    public AdminController()
    {
    }


    [HttpGet("test")]
    public async Task<IActionResult> SampleEndpoint()
    {
        return Ok("Det virkede :D");
    }
}