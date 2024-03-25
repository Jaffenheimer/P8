using System;

namespace p8_shared;

public class BusStop
{
    public Guid Id { get; set; }
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public int PeopleCount { get; set; }

    public BusStop()
    {
        
    }

    public BusStop(Guid id, double latitude, double longitude)
    {
        Id = id;
        Latitude = latitude;
        Longitude = longitude;
    }
}