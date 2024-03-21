using System;

namespace p8_shared;

public class Bus
{
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }
    public Guid Id { get; set; }
    public Action Action { get; set; }

    public Bus(decimal latitude, decimal longitude, Guid id)
    {
        Latitude = latitude;
        Longitude = longitude;
        Id = id;
    }
}