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

    public async Task<bool> UpsertRoute(Guid id, string password, List<Guid> busStopIds)
    {
        var query = $@"
            INSERT INTO {RouteTableName} (Id, Password, UpdatedAt)
            VALUES (@Id, @Password, @UpdatedAt)";

        var parameters = new
        {
            Id = id,
            Password = password,
            UpdatedAt = DateTime.UtcNow
        };
        
        if (await Connection.ExecuteAsync(query, parameters) > 0)
        {
            foreach (var busStopId in busStopIds)
            {
               var res = await UpsertRouteRelation(id, busStopId);

               if (!res)
                   return false;
            }
            return true;
        }
        return false;
    }

    private async Task<bool> UpsertRouteRelation(Guid routeId, Guid busStopId)
    {
        var query = $@"
            INSERT INTO {TableName} (RouteId, BusStopId, OrderNum)
            VALUES (@RouteId, @BusStopId, @OrderNum)";
        var query2 = $@"SELECT COALESCE(MAX(OrderNum), -1) FROM {TableName} WHERE RouteId = @RouteId";
        var orderNum = await Connection.QueryFirstOrDefaultAsync<int>(query2, new{RouteId = routeId});
        orderNum++;
        var parameters = new
        {
            RouteId = routeId,
            BusStopId = busStopId,
            OrderNum = orderNum
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

    public async Task<Guid?> GetRouteFromPassword(string password)
    {
        var query = $@"
            SELECT Id FROM {RouteTableName}
            WHERE Password = @Password";
        
        var result = await Connection.QueryFirstOrDefaultAsync<Guid>(query, new { Password = password });
        return result;
    }
}