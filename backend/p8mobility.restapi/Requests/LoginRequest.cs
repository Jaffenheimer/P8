namespace p8_restapi.Requests;

public class LoginRequest
{
    public string Username { get; set; }
    public string Password { get; set; }
    public string Country { get; set; }
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }

    public LoginRequest(string username, string password, decimal latitude, decimal longitude, string country)
    {
        Username = username;
        Password = password;
        Latitude = latitude;
        Longitude = longitude;
        Country = country;
    }
}