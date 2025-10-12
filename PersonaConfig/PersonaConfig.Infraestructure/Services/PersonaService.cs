using PersonaConfig.Infraestructure.Exceptions;
using PersonaConfig.Infraestructure.Models;
using System.Text.Json;

namespace PersonaConfig.Infraestructure.Services
{
    public sealed class PersonaService
    {
        private readonly HttpClient _httpClient;
        private readonly string _secret;

        public PersonaService()
        {
            var url = Environment.GetEnvironmentVariable("PERSONA_API_URL");
            if (string.IsNullOrEmpty(url))
                throw new PersonaServiceException("Environment variable PERSONA_API_URL is not set.");

            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(url),
                Timeout = TimeSpan.FromMinutes(1)
            };
            _httpClient.DefaultRequestHeaders.Accept.Clear();
            _httpClient.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

            var secret = Environment.GetEnvironmentVariable("PERSONA_API_SECRET");
            if (string.IsNullOrEmpty(secret))
                throw new PersonaServiceException("Environment variable PERSONA_API_SECRET is not set.");

            _secret = secret;
        }

        public IEnumerable<Persona> GetAll()
        {
            var response = _httpClient.GetAsync("personas").Result;
            if (!response.IsSuccessStatusCode)
                throw new PersonaServiceException("Error fetching personas");

            var content = response.Content.ReadAsStringAsync().Result;
            if (string.IsNullOrEmpty(content))
                return [];

            var apiResponse = JsonSerializer.Deserialize<PersonaServiceResponse<IEnumerable<Persona>>>(content);
            return apiResponse?.Source ?? [];
        }

        public Persona? GetById(int id)
        {
            var response = _httpClient.GetAsync($"persona/{id}").Result;
            if (!response.IsSuccessStatusCode)
                throw new PersonaServiceException("Error to get the persona");

            var content = response.Content.ReadAsStringAsync().Result;
            if (string.IsNullOrEmpty(content))
                return null;

            var apiResponse = JsonSerializer.Deserialize<PersonaServiceResponse<Persona>>(content);
            return apiResponse?.Source;
        }

        public void Add(Persona persona)
        {
            var jsonContent = JsonSerializer.Serialize(persona);
            var content = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json");

            content.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.PostAsync("persona", content).Result;
            if (!response.IsSuccessStatusCode)
                throw new PersonaServiceException("Error to add the persona");
        }

        public void Update(Persona persona)
        {
            var jsonContent = JsonSerializer.Serialize(persona);
            var content = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json");

            content.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.PutAsync($"persona/{persona.Id}", content).Result;
            if (!response.IsSuccessStatusCode)
                throw new PersonaServiceException("Error to update the persona");
        }
    }
}
