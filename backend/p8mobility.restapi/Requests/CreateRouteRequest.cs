using System;
using System.Collections.Generic;

namespace p8_restapi.Requests;

public class CreateRouteRequest
{
    public string Password { get; set; }
    public List<Guid> BusStopIds { get; set; }

    public CreateRouteRequest(string password, List<Guid> busStopIds)
    {
        Password = password;
        BusStopIds = busStopIds;
    }
}