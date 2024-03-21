using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using p8_shared;

namespace p8mobility.persistence.BusStopRepository;

public interface IBusStopRepository
{
    /// <summary>
    /// Get the current count of a bus stop
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    public Task<BusStop> GetPeopleCountFromId(Guid id);
    /// <summary>
    /// Delete a bus stop
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    public Task<bool> DeleteBusStop(Guid id);
    /// <summary>
    /// Create a busstop
    /// </summary>
    /// <param name="id"></param>
    /// <param name="latitude"></param>
    /// <param name="longitude"></param>
    /// <returns></returns>
    public Task<bool> UpsertBusStop(Guid id, decimal latitude, decimal longitude);

    public  Task<List<BusStop>> GetAllBusStops();
}