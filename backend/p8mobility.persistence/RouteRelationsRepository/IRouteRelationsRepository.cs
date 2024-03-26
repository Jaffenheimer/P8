using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace p8mobility.persistence.RouteRelationsRepository;

public interface IRouteRelationsRepository
{
    public Task<List<Guid>> GetBusStopIdsFromRouteId(Guid routeId);
    public Task<bool> UpsertRouteRelation(Guid routeId, Guid busStopId);
    public Task<bool> UpsertRoute(Guid id, string name);
    public Task<List<Guid>> GetRouteIds();
}