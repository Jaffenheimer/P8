using System;
using System.Collections.Generic;
using System.Data;
using System.Threading.Tasks;
using Dapper;
using p8_shared;
using p8mobility.persistence.Connection;
using Action = p8_shared.Action;

namespace p8mobility.persistence.BusRepository;

public class BusRepository : IBusRepository
{
    private static readonly string TableName = "Bus";
    private readonly IDbConnectionFactory _connectionFactory;
    private IDbConnection Connection => _connectionFactory.Connection;

    public BusRepository(IDbConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }

    public async Task<bool> Upsert(Guid id, decimal latitude, decimal longitude, Action action)
    {
        var query = $@"
            INSERT INTO {TableName} (Id, Latitude, Longitude, Action, UpdatedAt)
            VALUES (@Id, @Latitude, @Longitude, @Action, @UpdatedAt)
            ON CONFLICT (Id) DO UPDATE
            SET Latitude = @Latitude, Longitude = @Longitude, Action = @Action, UpdatedAt = @UpdatedAt";

        var parameters = new
        {
            Id = id,
            Latitude = latitude,
            Longitude = longitude,
            Action = action.ToString(),
            UpdatedAt = DateTime.UtcNow
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }
    
    public async Task<bool> UpdateBusLocation(Guid id, decimal latitude, decimal longitude)
    {
        var query = $@"
            UPDATE {TableName}
            SET Latitude = @Latitude, Longitude = @Longitude, UpdatedAt = @UpdatedAt
            WHERE Id = @Id";

        var parameters = new
        {
            Id = id,
            Latitude = latitude,
            Longitude = longitude,
            UpdatedAt = DateTime.UtcNow
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }
    
    public async Task<bool> UpdateBusAction(Guid id, Action action)
    {
        var query = $@"
            UPDATE {TableName}
            SET Action = @Action, UpdatedAt = @UpdatedAt
            WHERE Id = @Id";

        var parameters = new
        {
            Id = id,
            Action = action.ToString(),
            UpdatedAt = DateTime.UtcNow
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }

    public async Task<List<Bus>> GetAllBuses()
    {
        var query = $@"
            SELECT * FROM {TableName}";
        return (await Connection.QueryAsync<Bus>(query)).AsList();
    }
}