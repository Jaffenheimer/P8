namespace p8_restapi.Requests;

public class CreateBusRequest
{
    public string Password { get; set; }
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }

    public CreateBusRequest(string password, decimal latitude, decimal longitude)
    {
        Password = password;
        Latitude = latitude;
        Longitude = longitude;
    }
}