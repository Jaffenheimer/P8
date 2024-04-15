using System;

namespace p8_restapi.Requests
{
    public class UpdateBusLocationRequest
    {
        public Guid BusId { get; set; }
        public decimal Latitude { get; set; }
        public decimal Longitude { get; set; }

        public UpdateBusLocationRequest(Guid busId, decimal latitude, decimal longitude)
        {
            BusId = busId;
            Latitude = latitude;
            Longitude = longitude;
        }
    }
}