using System;

namespace p8_shared;

public class User
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string PasswordHash { get; set; }
    public string PasswordSalt { get; set; }

    public User(Guid id, string name, string passwordHash, string passwordSalt)
    {
        Id = id;
        Name = name;
        PasswordHash = passwordHash;
        PasswordSalt = passwordSalt;
    }
}