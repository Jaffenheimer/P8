using System;

namespace p8_shared;

public class User
{
    public Guid Id { get; set; }
    public string UserName { get; set; }
    public string PasswordHash { get; set; }
    public string PasswordSalt { get; set; }

    public User()
    {
        
    }
    public User(Guid id, string userName, string passwordHash, string passwordSalt)
    {
        Id = id;
        UserName = userName;
        PasswordHash = passwordHash;
        PasswordSalt = passwordSalt;
    }
}