using PersonaConfig.Infraestructure.Exceptions;
using PersonaConfig.Infraestructure.Models;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig
{
    public partial class FormPersonasList : Form
    {
        private readonly PersonaService _personaService;

        public FormPersonasList(PersonaService personaService)
        {
            InitializeComponent();
            MaximizeBox = false;

            _personaService = personaService;
            LoadPersonas();
        }

        private void buttonUpdatePersona_Click(object sender, EventArgs e)
        {
            var selectedPersona = comboBoxPersonas.SelectedItem as Persona;
            if (selectedPersona == null)
            {
                MessageBox.Show("Escolha um persona para ser alterado.");
                return;
            }

            Persona? persona = null;
            try
            {
                persona = _personaService.GetById(selectedPersona.Id);
            }
            catch (PersonaServiceUnauthorizedException)
            {
                MessageBox.Show($"O acesso ao servidor foi negado.");
            }
            catch (PersonaServiceNotFoundException)
            {
                MessageBox.Show($"Este persona não foi encontrado. Ele pode ter sido removido.");
            }
            catch (PersonaServiceException ex)
            {
                MessageBox.Show($"Não foi possível carregar o prompt do persona: {ex.Message}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ocorreu um erro inesperado ao carregar o prompt do persona: {ex.Message}");
            }

            if (persona is null)
                return;

            try
            {
                persona.SetPrompt(_personaService.GetPrompt(selectedPersona.Id));
            }
            catch (PersonaServiceUnauthorizedException)
            {
                MessageBox.Show($"O acesso ao servidor foi negado.");
            }
            catch (PersonaServiceNotFoundException)
            {
                MessageBox.Show($"Este persona não foi encontrado. Ele pode ter sido removido.");
            }
            catch (PersonaServiceException ex)
            {
                MessageBox.Show($"Não foi possível carregar o prompt do persona: {ex.Message}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ocorreu um erro inesperado ao carregar o prompt do persona: {ex.Message}");
            }

            if (string.IsNullOrEmpty(persona.Prompt))
                return;

            OpenConfigForm(persona);
        }

        private void buttonAddPersona_Click(object sender, EventArgs e)
            => OpenConfigForm(persona: null);

        private void LoadPersonas()
        {
            try
            {
                comboBoxPersonas.DataSource = _personaService.GetAll();
                comboBoxPersonas.DisplayMember = "Name";
                comboBoxPersonas.ValueMember = "Id";
            }
            catch (PersonaServiceException ex)
            {
                MessageBox.Show($"Não foi possível se comunicar com o servidor: {ex.Message}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ocorreu um erro inesperado: {ex.Message}");
            }
        }

        private void OpenConfigForm(Persona? persona)
        {
            using var formConfig = new FormPersonaConfig(_personaService, persona);
            if (formConfig.ShowDialog() == DialogResult.OK)
                LoadPersonas();
        }
    }
}
