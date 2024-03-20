using System;
using System.Data;
using System.Threading.Tasks;
using Dapper;
using p8_shared;
using p8mobility.persistence.Connection;


namespace p8mobility.persistence.UserRepository;

public class UserRepository : IUserRepository
{
    private static readonly string TableName = "Users";
    private readonly IDbConnectionFactory _connectionFactory;
    private HelperFunctions HelperFunctions { get; } = new HelperFunctions();
    private IDbConnection Connection => _connectionFactory.Connection;

    public UserRepository(IDbConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }
    public async Task<User> GetUser(string name)
    {
        var query = $@"SELECT * FROM {TableName} WHERE UserName = @UserName";
        return await Connection.QueryFirstOrDefaultAsync<User>(query, new { UserName = name });
    }
    
    public async Task<bool> Upsert(Guid id, string userName, string password)
    {
        //TODO: Check om user eksisterer
        var query =
            $@"INSERT INTO {TableName} (Id, UserName, PasswordHash, PasswordSalt, UpdatedAt)
                            VALUES (@Id, @UserName, @PasswordHash, @PasswordSalt, @UpdatedAt)";
        var salt = HelperFunctions.GenerateSalt();
        var parameters = new
        {
            Id = id,
            UserName = userName,
            PasswordHash = HelperFunctions.GenerateHash(password + salt),
            PasswordSalt = salt,
            UpdatedAt = DateTime.UtcNow,
        };
        return await Connection.ExecuteAsync(query, parameters) > 0;
    }

    
    public async Task<User> LogIn(string userName, string password)
    {
        var query = $@"SELECT * FROM {TableName} WHERE UserName = @userName";


        var result = await Connection.QueryFirstOrDefaultAsync(query, new { userName });

        if (result != null)
        {
            var salt = result.Password_salt;
            var passwordHash = HelperFunctions.GenerateHash(password + salt);
            if (passwordHash == result.Password_hash)
            {
                return await GetUser(userName);
            }
        }

        return null;
    }
    
    public async Task<bool> DeleteUser(User user)
    {
        var query = $@"DELETE FROM {TableName} WHERE UserName = @Name";
        var result = await Connection.ExecuteAsync(query, new { Name = user.Name });
        return result > 0;
    }
}