using Dapper;
using Microsoft.Extensions.DependencyInjection;
using p8mobility.persistence.Connection;
using p8mobility.persistence.Dapper;
using p8mobility.persistence.SampleRepository;


namespace p8mobility.persistence.Extensions;

public static class ServiceCollectionExtension
{
    public static IServiceCollection ConfigurePersistenceMySqlConnection(this IServiceCollection services,
        string? connectionString)
    {
        services.AddSingleton<IDbConnectionFactory>(new MySqlConnectionFactory(connectionString));

        // Add repositories
        services.AddScoped<ISampleRepository, SampleRepository.SampleRepository>();
        

        // Dapper
        SqlMapper.AddTypeHandler(new GuidTypeHandler());

        return services;
    }
}