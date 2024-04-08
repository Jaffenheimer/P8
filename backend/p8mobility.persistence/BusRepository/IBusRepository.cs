using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using p8_shared;
using Action = p8_shared.Action;

namespace p8mobility.persistence.BusRepository;

public interface IBusRepository
{
    public Task<List<Bus>> GetAllBuses();
    public Task<bool> Upsert(Guid id, Guid routeId, decimal latitude, decimal longitude, Action action);
    public Task<bool> UpdateBusAction(Guid id, Action action);
    public Task<bool> UpdateBusLocation(Guid id, decimal latitude, decimal longitude);
    public Task<bool> DeleteBus(Guid id);
}