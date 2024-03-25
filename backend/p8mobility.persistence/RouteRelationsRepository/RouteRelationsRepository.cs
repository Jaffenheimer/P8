using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Dapper;
using p8mobility.persistence.Connection;

namespace p8mobility.persistence.RouteRelationsRepository;

public class RouteRelationsRepository : IRouteRelationsRepository
{
    private static readonly string TableName = "RouteRelations";
    private static readonly string RouteTableName = "Route";
    private readonly IDbConnectionFactory _connectionFactory;
    private IDbConnection Connection => _connectionFactory.Connection;

    public RouteRelationsRepository(IDbConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }

    public async Task<bool> UpsertRoute(Guid id, string name)
    {
        var query = $@"
            INSERT INTO {RouteTableName} (Id, Name, UpdatedAt)
            VALUES (@Id, @Name, @UpdatedAt)";

        var parameters = new
        {
            Id = id,
            Name = name,
            UpdatedAt = DateTime.UtcNow
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }

    public async Task<bool> UpsertRouteRelation(Guid routeId, Guid busStopId, int orderNum)
    {
        var query = $@"
            INSERT INTO {TableName} (RouteId, BusStopId, OrderNum, UpdatedAt)
            VALUES (@RouteId, @BusStopId, @OrderNum, @UpdatedAt)";

        var parameters = new
        {
            RouteId = routeId,
            BusStopId = busStopId,
            OrderNum = orderNum,
            UpdatedAt = DateTime.UtcNow
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }

    public async Task<List<Guid>> GetBusStopIdsFromRouteId(Guid routeId)
    {
        var query = $@"
            SELECT BusStopId FROM {TableName}
            WHERE RouteId = @RouteId";

        var parameters = new
        {
            RouteId = routeId
        };
        return (await Connection.QueryAsync<Guid>(query, parameters)).ToList();
    }

    public async Task<List<Guid>> GetRouteIds()
    {
        var query = $@"
            SELECT Id FROM {RouteTableName}";

        return (await Connection.QueryAsync<Guid>(query)).AsList();
    }
}