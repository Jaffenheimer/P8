using System;

namespace p8_restapi.Requests
{
    public class StopRequest
    {
        public Guid Id { get; set; }
        public double Latitude { get; set; }
        public double Longitude { get; set; }
        public int PeopleCount { get; set; }
        private DateTime _timestamp = DateTime.UtcNow;
    }
}
