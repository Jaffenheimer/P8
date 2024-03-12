using System.Data;

namespace p8mobility.persistence.Connection;

public interface IDbConnectionFactory
{
    public IDbConnection Connection { get; }
}