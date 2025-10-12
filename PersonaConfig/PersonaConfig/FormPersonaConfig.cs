using PersonaConfig.Infraestructure.Models;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig
{
    public partial class FormPersonaConfig : Form
    {
        private readonly PersonaService _service;
        private Persona? _persona;

        public FormPersonaConfig(PersonaService service, Persona? persona)
        {
            InitializeComponent();
            MaximizeBox = false;

            _service = service;
            _persona = persona;

            PopulateFields();
        }

        private void PopulateFields()
        {
            if (_persona is null)
                return;

            textBoxPersonaName.Text = _persona.Name;
            richTextBoxPersonaPrompt.Text = _persona.Prompt;
        }

        private void buttonSavePersona_Click(object sender, EventArgs e)
        {
            if (_persona is null)
            {
                var newPersona = new Persona(textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);
                _service.Add(newPersona);
            }
            else
            {
                var updatedPersona = new Persona(_persona.Id, textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);
                _service.Update(updatedPersona);
            }

            DialogResult = DialogResult.OK;
            Close();
        }
    }
}
