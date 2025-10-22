using PersonaConfig.Infraestructure.Exceptions;
using System.Text.Json.Serialization;

namespace PersonaConfig.Infraestructure.Models
{
    public class Persona
    {
        [JsonPropertyName("id")]
        public int Id { get; private set; }

        [JsonPropertyName("name")]
        public string Name { get; private set; }

        [JsonPropertyName("prompt")]
        public string Prompt { get; private set; }

        [JsonPropertyName("fileName")]
        public string? FileName { get; private set; }

        [JsonPropertyName("image")]
        public string? Image { get; private set; }

        public Persona(string name, string prompt)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new PersonaException("Name cannot be null or empty.");

            Name = name;
            Prompt = prompt;
        }

        public Persona(int id, string name, string prompt) : this(name, prompt)
        {
            if (id <= 0)
                throw new PersonaException("Id must be greater than zero.");

            Id = id;
        }

        [JsonConstructor]
        public Persona(int id, string name, string prompt, string fileName, string image) : this(id, name, prompt)
        {
            FileName = fileName;
            Image = image;
        }
    }
}
