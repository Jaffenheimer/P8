using System;

namespace p8_shared;

public class BusStop
{
    public Guid Id { get; set; }
    public decimal Latitude { get; set; }
    public decimal Longitude { get; set; }
    public int PeopleCount { get; set; }
    public int OrderNum { get; set; }

    public BusStop()
    {
    }

    public BusStop(Guid id, decimal latitude, decimal longitude, int peopleCount, int orderNum)
    {
        Id = id;
        Latitude = latitude;
        Longitude = longitude;
        PeopleCount = peopleCount;
        OrderNum = orderNum;
    }
}