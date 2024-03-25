using System;

namespace p8_restapi.Requests
{
    public class StopRequest
    {
        private DateTime _timestamp = DateTime.UtcNow;
        public int PeopleCount { get; set; }
    }
}