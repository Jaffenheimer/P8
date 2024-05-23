using System;
using System.Collections.Generic;
using Action = p8_shared.Action;

namespace p8_restapi.Requests;

public class PusherRequest
{
    public List<Guid> Ids { get; set; }
    public List<Action> Actions { get; set; }
}