using PersonaConfig.Infraestructure.Exceptions;
using PersonaConfig.Infraestructure.Models;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig
{
    public partial class FormPersonaConfig : Form
    {
        private readonly PersonaService _service;
        private string _buttonSavePersonaOriginalText;
        private readonly Persona? _persona;

        public FormPersonaConfig(PersonaService service, Persona? persona)
        {
            InitializeComponent();
            MaximizeBox = false;
            _buttonSavePersonaOriginalText = buttonSavePersona.Text;

            _service = service;
            _persona = persona;

            PopulateFields();
        }

        private void buttonSavePersona_Click(object sender, EventArgs e)
        {
            if (!PersonaIsValid())
                return;

            SetButtonState(false);

            bool success;
            if (_persona is null)
            {
                var newPersona = new Persona(textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);
                success = HandleServiceAction(() => _service.Add(newPersona));
            }
            else
            {
                var updatedPersona = new Persona(_persona.Id, textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);
                success = HandleServiceAction(() => _service.Update(updatedPersona));
            }

            SetButtonState(true);

            if (!success)
                return;

            DialogResult = DialogResult.OK;
            Close();
        }

        private void buttonDeletePersona_Click(object sender, EventArgs e)
        {
            // ask for confirmation
            var result = MessageBox.Show("Tem certeza que deseja excluir este persona?", "Confirmação", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (result != DialogResult.Yes)
                return;

            if (_persona is null)
                return;

            SetButtonState(false);

            bool success = HandleServiceAction(() => _service.Delete(_persona.Id));

            SetButtonState(true);

            if (!success)
                return;

            DialogResult = DialogResult.OK;
            Close();
        }

        private static bool HandleServiceAction(Action action)
        {
            try
            {
                action();
                return true;
            }
            catch (PersonaServiceException ex)
            {
                MessageBox.Show($"Não foi possível se comunicar com o servidor: {ex.Message}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ocorreu um erro inesperado: {ex.Message}");
            }

            return false;
        }

        private void PopulateFields()
        {
            if (_persona is null)
                return;

            textBoxPersonaName.Text = _persona.Name;
            richTextBoxPersonaPrompt.Text = _persona.Prompt;
            buttonDeletePersona.Visible = true;
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
                MessageBox.Show(string.Join(Environment.NewLine, messages), "Atenção", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return false;
            }

            return true;
        }

        private void SetButtonState(bool enabled)
        {
            buttonSavePersona.Enabled = enabled;
            buttonDeletePersona.Enabled = enabled;
            buttonSavePersona.Text = enabled ? _buttonSavePersonaOriginalText : "Aguarde";
            Cursor = enabled ? Cursors.Default : Cursors.WaitCursor;
        }
    }
}
