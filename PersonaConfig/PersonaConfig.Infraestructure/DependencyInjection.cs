using Microsoft.Extensions.DependencyInjection;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig.Infraestructure
{
    public static class DependencyInjection
    {
        public static void RegisterInfraServices(this ServiceCollection services)
        {
            services.AddSingleton<PersonaService>();
        }
    }
}
