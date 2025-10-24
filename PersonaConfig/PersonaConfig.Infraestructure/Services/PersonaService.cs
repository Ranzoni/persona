using PersonaConfig.Infraestructure.Exceptions;
using PersonaConfig.Infraestructure.Models;
using System.Net;
using System.Net.Http.Json;
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
            var response = _httpClient.GetAsync("persona").Result;
            return HandleResponse<IEnumerable<Persona>>(response, "Error fetching personas") ?? [];
        }

        public Persona? GetById(int id)
        {
            var response = _httpClient.GetAsync($"persona/{id}").Result;
            return HandleResponse<Persona>(response, "Error to get the persona");
        }

        public string? GetPrompt(int id)
        {
            var request = new HttpRequestMessage(HttpMethod.Get, $"persona/{id}/prompt");
            request.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.SendAsync(request).Result;
            return HandleResponse<string>(response, "Error to get the persona prompt");
        }

        public Persona? Add(Persona persona)
        {
            var jsonContent = JsonSerializer.Serialize(persona);
            var content = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json");

            content.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.PostAsync("persona", content).Result;
            return HandleResponse<Persona>(response, "Error to add the persona");
        }

        public void Update(Persona persona)
        {
            var jsonContent = JsonSerializer.Serialize(persona);
            var content = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json");

            content.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.PutAsync($"persona/{persona.Id}", content).Result;
            HandleResponse<Persona>(response, "Error to update the persona");
        }

        public void Delete(int id)
        {
            var request = new HttpRequestMessage(HttpMethod.Delete, $"persona/{id}");
            request.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.SendAsync(request).Result;
            HandleResponse<string>(response, "Error to delete the persona");
        }

        public void UploadImage(int personaId, byte[] image, string fileName, string fileExtension)
        {
            using var content = new MultipartFormDataContent();
            var imageContent = new ByteArrayContent(image);
            imageContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue($"image/{fileExtension}");

            content.Add(imageContent, "file", fileName);

            content.Headers.Add("X-Secret-Key", _secret);
            var response = _httpClient.PostAsync($"persona/{personaId}/upload", content).Result;
            HandleResponse<string>(response, "Error to upload the persona image");
        }

        private static T? HandleResponse<T>(HttpResponseMessage response, string errorResponseMessage)
        {
            if (!response.IsSuccessStatusCode)
                throw new PersonaServiceException(errorResponseMessage);

            var content = response.Content.ReadAsStringAsync().Result;
            var apiResponse = JsonSerializer.Deserialize<PersonaServiceResponse<T>>(content);

            if (apiResponse is null || !apiResponse.Success || apiResponse.Source is null)
                throw new PersonaServiceException(errorResponseMessage);

            return apiResponse.Source;
        }
    }
}
