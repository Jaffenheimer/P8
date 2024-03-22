namespace p8_restapi.Requests;

public class CreateUserRequest
{
    public string Username { get; set; }
    public string Password { get; set; }

    public CreateUserRequest(string username, string password)
    {
        Username = username;
        Password = password;
    }
}