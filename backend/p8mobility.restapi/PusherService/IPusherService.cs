using p8_shared;

namespace p8_restapi.PusherService
{
    public interface IPusherService
    {
        void PublishAction(string channel, string eventName, PusherMessage data);
    }
}

