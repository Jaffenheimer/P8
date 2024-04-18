using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using p8_restapi.PusherService;
using p8mobility.persistence.Extensions;

namespace p8_restapi
{
    namespace Translation.RestApi
    {
        public class Startup
        {
            private const string ServiceName = "P8.RestApi";
            private const string SwaggerRoute = "restApi";

            public Startup(IConfiguration configuration)
            {
                Configuration = configuration;
            }

            public IConfiguration Configuration { get; }

            // This method gets called by the runtime. Use this method to add services to the container.
            public void ConfigureServices(IServiceCollection services)
            {
                IMvcBuilder mvcBuilder = services.AddControllers();
                mvcBuilder.AddJsonOptions(options =>
                {
                    options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
                });
                services.AddSwaggerGen(s =>
                {
                    s.SwaggerDoc("v1", new OpenApiInfo {Title = ServiceName, Version = "v1"});
                });

                services.Configure<PusherConfiguration>(Configuration.GetSection("Pusher"));
                services.AddOptions();
                services.AddSingleton<IPusherService, PusherService.PusherService>();
                services.ConfigurePersistenceMySqlConnection(Configuration.GetConnectionString("MySqlDatabase"));
                
            }

            // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
            public void Configure(IApplicationBuilder program, IWebHostEnvironment env)
            {
                if (env.IsDevelopment())
                {
                    program.UseDeveloperExceptionPage();
                }

                program.UseSwagger(s => { s.RouteTemplate = $"/{SwaggerRoute}" + "/{documentName}/swagger.json"; });
                program.UseSwaggerUI(s =>
                {
                    s.SwaggerEndpoint($"/{SwaggerRoute}/v1/swagger.json", "v1");
                    s.RoutePrefix = $"{SwaggerRoute}/swagger";
                });

                program.UseRouting();
                program.UseCors(x => x.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
                program.UseEndpoints(endpoints => { endpoints.MapControllers(); });
            }
        }
    }
}