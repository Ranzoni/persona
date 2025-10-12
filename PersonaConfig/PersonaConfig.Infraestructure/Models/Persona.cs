using System.Text.Json.Serialization;

namespace PersonaConfig.Infraestructure.Models
{
    public class Persona(string name, string prompt)
    {
        [JsonPropertyName("id")]
        public int Id { get; private set; }

        [JsonPropertyName("name")]
        public string Name { get; private set; } = name;

        [JsonPropertyName("prompt")]
        public string Prompt { get; private set; } = prompt;

        [JsonConstructor]
        public Persona(int id, string name, string prompt) : this(name, prompt)
        {
            Id = id;
        }
    }
}
