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

            var persona = _personaService.GetById(selectedPersona.Id);
            if (persona == null)
            {
                MessageBox.Show("Não foi possível carregar o persona selecionado.");
                return;
            }

            persona.SetPrompt(_personaService.GetPrompt(selectedPersona.Id));
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
