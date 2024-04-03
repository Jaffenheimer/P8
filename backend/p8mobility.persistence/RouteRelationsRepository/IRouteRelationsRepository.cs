using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace p8mobility.persistence.RouteRelationsRepository;

public interface IRouteRelationsRepository
{
    public Task<List<Guid>> GetBusStopIdsFromRouteId(Guid routeId);
    public Task<bool> UpsertRoute(Guid id, string password, List<Guid> busStopIds);
    public Task<List<Guid>> GetRouteIds();
    public Task<Guid?> GetRouteFromPassword(string password);
}