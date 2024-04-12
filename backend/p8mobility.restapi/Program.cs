using System.Threading;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using p8_restapi.Translation.RestApi;

namespace p8_restapi
{
    public class Program
    {
        public static StateController.StateController _stateController;
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                    webBuilder.UseUrls("http://192.168.1.125:5000");
                }).ConfigureServices(services =>
                {
                    _stateController = new StateController.StateController();
                    services.AddSingleton(_stateController);
                });

    }
}