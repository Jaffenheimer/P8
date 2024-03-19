using System;
using System.Threading.Tasks;
using p8_shared;

namespace p8mobility.persistence.UserRepository;

public interface IUserRepository
{
    /// <summary>
    /// Gets a user by username
    /// </summary>
    /// <param name="name"></param>
    /// <returns>Returns a user if found in the database otherwise 0</returns>
    public Task<User> GetUser(string name);

    /// <summary>
    /// Creates a user and store it in the database
    /// </summary>
    /// <param name="id"></param>
    /// <param name="userName"></param>
    /// <param name="password"></param>
    /// <returns>Returns true if successful E.g the number of rows affected is more than 0, otherwise false</returns>
    public Task<bool> Upsert(Guid id, string userName, string password);

    /// <summary>
    /// Login a user by username and password
    /// </summary>
    /// <param name="userName"></param>
    /// <param name="password"></param>
    /// <returns>Returns a user if the login was successful, otherwise null</returns>
    public Task<User> LogIn(string userName, string password);

    /// <summary>
    /// Deletes a user from the database
    /// </summary>
    /// <param name="user"></param>
    /// <returns>Returns true if it went well otherwise false</returns>
    public Task<bool> DeleteUser(User user);
}