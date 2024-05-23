using p8_shared;
using System.Threading.Tasks;

namespace p8_restapi.PusherService
{
    public interface IPusherService
    {
        Task<bool> PublishAction(string channel, string eventName, PusherMessage data);
    }
}