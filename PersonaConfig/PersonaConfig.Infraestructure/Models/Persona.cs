using PersonaConfig.Infraestructure.Exceptions;
using System.Text.Json.Serialization;

namespace PersonaConfig.Infraestructure.Models
{
    public class Persona
    {
        private int _id;
        private string _name = string.Empty;

        [JsonPropertyName("id")]
        public int Id
        {
            get => _id;
            private set
            {
                if (value <= 0)
                    throw new PersonaException("Id must be greater than zero.");

                _id = value;
            }
        }

        [JsonPropertyName("name")]
        public string Name
        { 
            get => _name;
            private set
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new PersonaException("Name cannot be null or empty.");

                _name = value;
            }
        }

        [JsonPropertyName("prompt")]
        public string? Prompt { get; private set; }

        [JsonPropertyName("fileName")]
        public string? FileName { get; private set; }

        [JsonPropertyName("image")]
        public string? Image { get; private set; }

        public Persona(string name, string prompt)
        {
            Name = name;
            Prompt = prompt;
        }

        public Persona(int id, string name, string prompt) : this(name, prompt)
            => Id = id;

        [JsonConstructor]
        public Persona(int id, string name, string fileName, string image)
        {
            Id = id;
            Name = name;
            FileName = fileName;
            Image = image;
        }

        public void SetPrompt(string? prompt)
            => Prompt = prompt;
    }
}
