using System;
using System.Collections.Generic;

namespace p8_shared;

public class PusherMessage
{
    public Dictionary<Guid, Action> Actions { get; set; }

    public PusherMessage(Dictionary<Guid, Action> actions)
    {
        Actions = actions;
    }
}