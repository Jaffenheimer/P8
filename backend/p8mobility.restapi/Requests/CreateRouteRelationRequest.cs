using System;

namespace p8_restapi.Requests;

public class CreateRouteRelationRequest
{
    public Guid RouteId { get; set; }
    public Guid BusStopId { get; set; }

    public CreateRouteRelationRequest(Guid routeId, Guid busStopId)
    {
        RouteId = routeId;
        BusStopId = busStopId;
    }
}