using System;

namespace p8_restapi.Requests
{
    public class StopRequest
    {
        public Guid Id { get; set; }
        public decimal Latitude { get; set; }
        public decimal Longitude { get; set; }
        public int PeopleCount { get; set; }

        private DateTime _timestamp = DateTime.UtcNow;
    }
}