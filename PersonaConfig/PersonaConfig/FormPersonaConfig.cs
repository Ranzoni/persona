using PersonaConfig.Infraestructure.Models;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig
{
    public partial class FormPersonaConfig : Form
    {
        private readonly PersonaService _service;
        private readonly Persona? _persona;

        public FormPersonaConfig(PersonaService service, Persona? persona)
        {
            InitializeComponent();
            MaximizeBox = false;

            _service = service;
            _persona = persona;

            PopulateFields();
        }

        private void buttonSavePersona_Click(object sender, EventArgs e)
        {
            if (!PersonaIsValid())
                return;

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

        private void PopulateFields()
        {
            if (_persona is null)
                return;

            textBoxPersonaName.Text = _persona.Name;
            richTextBoxPersonaPrompt.Text = _persona.Prompt;
        }

        private bool PersonaIsValid()
        {
            var messages = new List<string>();
            if (string.IsNullOrWhiteSpace(textBoxPersonaName.Text))
                messages.Add("O nome do persona não foi preenchido.");

            if (string.IsNullOrWhiteSpace(richTextBoxPersonaPrompt.Text))
                messages.Add("O prompt do persona não foi preenchido.");

            if (messages.Count != 0)
            {
                MessageBox.Show(string.Join(Environment.NewLine, messages), "Atenção", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }
            
            return true;
        }
    }
}
