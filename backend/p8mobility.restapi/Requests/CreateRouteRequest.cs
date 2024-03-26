namespace p8_restapi.Requests;

public class CreateRouteRequest
{
    public string Name { get; set; }

    public CreateRouteRequest(string name)
    {
        Name = name;
    }
}