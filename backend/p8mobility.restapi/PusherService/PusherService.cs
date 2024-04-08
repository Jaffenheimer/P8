using System.Text.Json;
using Microsoft.Extensions.Options;
using p8_shared;
using PusherServer;

namespace p8_restapi.PusherService
{
    public class PusherService : IPusherService
    {
        private readonly IOptions<PusherConfiguration> _pusherConfiguration;

        public PusherService(IOptions<PusherConfiguration> pusherConfiguration) {
            _pusherConfiguration = pusherConfiguration;
        }
        
        public async void PublishAction(string channel, string eventName, PusherMessage data)
        {
            var pusher = new Pusher(_pusherConfiguration.Value.AppId, _pusherConfiguration.Value.Key, _pusherConfiguration.Value.Secret, new PusherOptions
            {
                Cluster = _pusherConfiguration.Value.Cluster
            });
            await pusher.TriggerAsync(channel, eventName, JsonSerializer.Serialize(data));
        }
    }
}