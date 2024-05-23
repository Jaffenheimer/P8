using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using p8_restapi.PusherService;
using p8_restapi.Translation.RestApi;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;

namespace p8_restapi
{
    public class Program
    {
        public static StateController.StateController _stateController;
        public static string hostName = Dns.GetHostName();
        public static IPHostEntry ip = Dns.GetHostEntry(hostName); 

        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                    if(OperatingSystem.IsMacOS())
                        webBuilder.UseUrls("http://" + ip.AddressList[0] + ":5000");
                    if(OperatingSystem.IsWindows())
                        webBuilder.UseUrls("http://" + "192.168.1.182" + ":5000");
                    if (OperatingSystem.IsLinux())
                        webBuilder.UseUrls("http://" + ip.AddressList[1] + ":5000");
                }).ConfigureServices(services =>
                {
                    _stateController = new StateController.StateController();
                    services.AddSingleton(_stateController);
                    _stateController
                        .Init(
                            services.BuildServiceProvider().GetService<IBusStopRepository>() ??
                            throw new InvalidOperationException(),
                            services.BuildServiceProvider().GetService<IRouteRelationsRepository>() ??
                            throw new InvalidOperationException(),
                            services.BuildServiceProvider().GetService<IPusherService>()).Wait();
                    //new Thread(() => _stateController.Run(services.BuildServiceProvider().GetService<IPusherService>() ?? throw new InvalidOperationException())).Start();
                });
    }
}