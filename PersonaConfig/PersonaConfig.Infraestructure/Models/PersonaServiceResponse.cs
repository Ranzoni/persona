using System.Text.Json.Serialization;

namespace PersonaConfig.Infraestructure.Models
{
    internal class PersonaServiceResponse<T>
    {
        [JsonPropertyName("success")]
        public bool Success { get; set; }

        [JsonPropertyName("source")]
        public T? Source { get; set; }
    }
}
