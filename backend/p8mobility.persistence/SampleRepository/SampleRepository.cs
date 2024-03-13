using System.Data;

using p8mobility.persistence.Connection;

namespace p8mobility.persistence.SampleRepository;

public class SampleRepository : ISampleRepository
{
    private static readonly string TableName = "";
    private readonly IDbConnectionFactory _connectionFactory;
    private IDbConnection Connection => _connectionFactory.Connection;

    public SampleRepository(IDbConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }
}