namespace p8_restapi.Requests;

public class CreateBusStopRequest
{
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }

    public CreateBusStopRequest(decimal latitude, decimal longitude)
    {
        Latitude = latitude;
        Longitude = longitude;
    }
}