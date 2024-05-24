using System;

namespace p8_restapi.Requests
{
    public class UpdatePeopleCountRequest
    {
        public int PeopleCount { get; set; }
        public Guid Id { get; set; }
        public UpdatePeopleCountRequest(int peopleCount, Guid id)
        {
            PeopleCount = peopleCount;
            Id = id;
        }
    }
}
