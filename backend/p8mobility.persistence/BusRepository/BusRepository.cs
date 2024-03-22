using System.Data;
using p8mobility.persistence.Connection;

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
}