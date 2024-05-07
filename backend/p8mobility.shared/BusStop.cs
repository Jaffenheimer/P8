using System;

namespace p8_shared;

public class BusStop
{
    public Guid Id { get; set; }
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }
    public int PeopleCount { get; set; }

    public DateTime UpdatedAt { get; set; }

    public BusStop()
    {
    }

    public BusStop(Guid id, decimal latitude, decimal longitude, int peopleCount)
    {
        Id = id;
        Latitude = latitude;
        Longitude = longitude;
        PeopleCount = peopleCount;
    }
}