using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using p8_shared;
using Action = p8_shared.Action;

namespace p8mobility.persistence.BusRepository;

public interface IBusRepository
{
    public Task<List<Bus>> GetAllBuses();
    public Task<bool> Upsert(Guid id, decimal latitude, decimal longitude, Action action);
}