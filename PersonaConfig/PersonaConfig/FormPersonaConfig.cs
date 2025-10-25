using PersonaConfig.Infraestructure.Exceptions;
using PersonaConfig.Infraestructure.Models;
using PersonaConfig.Infraestructure.Services;

namespace PersonaConfig
{
    public partial class FormPersonaConfig : Form
    {
        private readonly PersonaService _service;
        private readonly string _buttonSavePersonaOriginalText;
        private readonly Persona? _persona;

        public bool EditMode { get => _persona is not null; }

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
            if (EditMode)
                success = UpdatePersona();
            else
                success = CreatePersona();

            SetButtonState(true);

            if (!success)
                return;

            DialogResult = DialogResult.OK;
            Close();
        }

        private bool CreatePersona()
        {
            var newPersona = new Persona(textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);

            Persona? personaCreated = null;
            var success = HandleServiceAction(() =>
            {
                try
                {
                    personaCreated = _service.Add(newPersona);
                    return true;
                }
                catch (PersonaServiceUnauthorizedException ex)
                {
                    throw new PersonaServiceUnauthorizedException(ex.Message);
                }
                catch (PersonaServiceConflictException)
                {
                    MessageBox.Show($"Este persona já existe.");
                }
                catch (PersonaServiceException ex)
                {
                    throw new PersonaServiceException(ex.Message);
                }
                catch (Exception ex)
                {
                    throw new Exception(ex.Message);
                }

                return false;
            });
            if (!success || personaCreated is null)
                return false;

            if (!UploadImage(personaCreated))
            {
                try
                {
                    _service.Delete(personaCreated.Id);
                }
                catch (Exception)
                {
                }

                return false;
            }

            return true;
        }

        private bool UpdatePersona()
        {
            if (_persona is null)
            {
                MessageBox.Show("Não foi informado um persona para alteração.");
                return false;
            }

            var uploadSuccess = UploadImage(_persona);
            if (!uploadSuccess)
            {
                MessageBox.Show("Não foi possível extrair a imagem do persona.");
                return false;
            }

            var updatedPersona = new Persona(_persona.Id, textBoxPersonaName.Text, richTextBoxPersonaPrompt.Text);
            return HandleServiceAction(() =>
            {
                try
                {
                    _service.Update(updatedPersona);
                    return true;
                }
                catch (PersonaServiceUnauthorizedException ex)
                {
                    throw new PersonaServiceUnauthorizedException(ex.Message);
                }
                catch (PersonaServiceConflictException)
                {
                    MessageBox.Show($"Este persona já existe.");
                }
                catch (PersonaServiceNotFoundException)
                {
                    MessageBox.Show($"Este persona não foi encontrado. Ele pode ter sido removido.");
                }
                catch (PersonaServiceException ex)
                {
                    throw new PersonaServiceException(ex.Message);
                }
                catch (Exception ex)
                {
                    throw new Exception(ex.Message);
                }

                return false;
            });
        }

        private bool UploadImage(Persona persona)
        {
            if (persona is null || pbPersonaImg.Image is null)
                return false;

            using var ms = new MemoryStream();
            pbPersonaImg.Image.Save(ms, pbPersonaImg.Image.RawFormat);
            var imageBytes = ms.ToArray();
            var fileExtension = Path.GetExtension(labelImgName.Text).TrimStart('.').ToLower();
            return HandleServiceAction(() =>
            {
                try
                {
                    _service.UploadImage(persona.Id, imageBytes, labelImgName.Text, fileExtension);
                    return true;
                }
                catch (PersonaServiceUnauthorizedException ex)
                {
                    throw new PersonaServiceUnauthorizedException(ex.Message);
                }
                catch (PersonaServiceNotFoundException)
                {
                    MessageBox.Show($"Este persona não foi encontrado. Ele pode ter sido removido.");
                }
                catch (PersonaServiceException ex)
                {
                    throw new PersonaServiceException(ex.Message);
                }
                catch (Exception ex)
                {
                    throw new Exception(ex.Message);
                }

                return false;
            });
        }

        private void buttonDeletePersona_Click(object sender, EventArgs e)
        {
            var result = MessageBox.Show("Tem certeza que deseja excluir este persona?", "Confirmação", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (result != DialogResult.Yes)
                return;

            if (_persona is null)
                return;

            SetButtonState(false);

            var success = HandleServiceAction(() =>
            {
                try
                {
                    _service.Delete(_persona.Id);
                    return true;
                }
                catch (PersonaServiceUnauthorizedException ex)
                {
                    throw new PersonaServiceUnauthorizedException(ex.Message);
                }
                catch (PersonaServiceNotFoundException)
                {
                    MessageBox.Show($"Este persona não foi encontrado. Ele pode ter sido removido.");
                }
                catch (PersonaServiceException ex)
                {
                    throw new PersonaServiceException(ex.Message);
                }
                catch (Exception ex)
                {
                    throw new Exception(ex.Message);
                }

                return false;
            });

            SetButtonState(true);

            if (!success)
                return;

            DialogResult = DialogResult.OK;
            Close();
        }

        private static bool HandleServiceAction(Func<bool> action)
        {
            try
            {
                return action();
            }
            catch (PersonaServiceUnauthorizedException)
            {
                MessageBox.Show($"O acesso ao servidor foi negado.");
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
            if (!EditMode)
                return;

            textBoxPersonaName.Text = _persona?.Name;
            richTextBoxPersonaPrompt.Text = _persona?.Prompt;
            labelImgName.Text = Path.GetFileName(_persona?.FileName);
            if (!string.IsNullOrEmpty(_persona?.Image))
            {
                pbPersonaImg.Load(_persona.Image);
                labelImgName.Visible = true;
            }
            buttonDeletePersona.Visible = true;
        }

        private bool PersonaIsValid()
        {
            var messages = new List<string>();
            if (string.IsNullOrWhiteSpace(textBoxPersonaName.Text))
                messages.Add("O nome do persona não foi preenchido.");

            if (string.IsNullOrWhiteSpace(richTextBoxPersonaPrompt.Text))
                messages.Add("O prompt do persona não foi preenchido.");

            if (pbPersonaImg.Image is null)
                messages.Add("A imagem do persona não foi carregada.");

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

        private void buttonUploadImg_Click(object sender, EventArgs e)
        {
            var openFileDialog = new OpenFileDialog
            {
                Filter = "Image Files|*.jpg;*.jpeg;*.png;*.gif;*.bmp|All Files|*.*",
                Title = "Select an Image File"
            };

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    pbPersonaImg.Image = Image.FromFile(openFileDialog.FileName);
                    pbPersonaImg.SizeMode = PictureBoxSizeMode.Zoom;

                    labelImgName.Text = Path.GetFileName(openFileDialog.FileName);
                    labelImgName.Visible = true;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Falha ao carregar a imagem: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
    }
}
