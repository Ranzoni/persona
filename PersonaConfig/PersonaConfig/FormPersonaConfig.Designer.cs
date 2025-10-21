namespace PersonaConfig
{
    partial class FormPersonaConfig
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            textBoxPersonaName = new TextBox();
            richTextBoxPersonaPrompt = new RichTextBox();
            buttonSavePersona = new Button();
            labelPersonaName = new Label();
            labelPersonaPrompt = new Label();
            buttonDeletePersona = new Button();
            pbPersonaImg = new PictureBox();
            buttonUploadImg = new Button();
            labelImgName = new Label();
            ((System.ComponentModel.ISupportInitialize)pbPersonaImg).BeginInit();
            SuspendLayout();
            // 
            // textBoxPersonaName
            // 
            textBoxPersonaName.Location = new Point(12, 155);
            textBoxPersonaName.Name = "textBoxPersonaName";
            textBoxPersonaName.Size = new Size(400, 23);
            textBoxPersonaName.TabIndex = 0;
            // 
            // richTextBoxPersonaPrompt
            // 
            richTextBoxPersonaPrompt.Location = new Point(12, 205);
            richTextBoxPersonaPrompt.Name = "richTextBoxPersonaPrompt";
            richTextBoxPersonaPrompt.Size = new Size(400, 193);
            richTextBoxPersonaPrompt.TabIndex = 1;
            richTextBoxPersonaPrompt.Text = "";
            // 
            // buttonSavePersona
            // 
            buttonSavePersona.Location = new Point(335, 410);
            buttonSavePersona.Name = "buttonSavePersona";
            buttonSavePersona.Size = new Size(75, 23);
            buttonSavePersona.TabIndex = 2;
            buttonSavePersona.Text = "Salvar";
            buttonSavePersona.UseVisualStyleBackColor = true;
            buttonSavePersona.Click += buttonSavePersona_Click;
            // 
            // labelPersonaName
            // 
            labelPersonaName.AutoSize = true;
            labelPersonaName.Location = new Point(12, 137);
            labelPersonaName.Name = "labelPersonaName";
            labelPersonaName.Size = new Size(40, 15);
            labelPersonaName.TabIndex = 3;
            labelPersonaName.Text = "Nome";
            // 
            // labelPersonaPrompt
            // 
            labelPersonaPrompt.AutoSize = true;
            labelPersonaPrompt.Location = new Point(10, 187);
            labelPersonaPrompt.Name = "labelPersonaPrompt";
            labelPersonaPrompt.Size = new Size(47, 15);
            labelPersonaPrompt.TabIndex = 4;
            labelPersonaPrompt.Text = "Prompt";
            // 
            // buttonDeletePersona
            // 
            buttonDeletePersona.BackColor = SystemColors.Control;
            buttonDeletePersona.Image = Properties.Resources.trash;
            buttonDeletePersona.Location = new Point(12, 404);
            buttonDeletePersona.Name = "buttonDeletePersona";
            buttonDeletePersona.Size = new Size(30, 29);
            buttonDeletePersona.TabIndex = 5;
            buttonDeletePersona.UseVisualStyleBackColor = false;
            buttonDeletePersona.Visible = false;
            buttonDeletePersona.Click += buttonDeletePersona_Click;
            // 
            // pbPersonaImg
            // 
            pbPersonaImg.Location = new Point(218, 12);
            pbPersonaImg.Name = "pbPersonaImg";
            pbPersonaImg.Size = new Size(125, 125);
            pbPersonaImg.TabIndex = 6;
            pbPersonaImg.TabStop = false;
            // 
            // buttonUploadImg
            // 
            buttonUploadImg.Location = new Point(37, 72);
            buttonUploadImg.Name = "buttonUploadImg";
            buttonUploadImg.Size = new Size(147, 23);
            buttonUploadImg.TabIndex = 7;
            buttonUploadImg.Text = "Carregar imagem";
            buttonUploadImg.UseVisualStyleBackColor = true;
            buttonUploadImg.Click += buttonUploadImg_Click;
            // 
            // labelImgName
            // 
            labelImgName.AutoSize = true;
            labelImgName.Location = new Point(37, 54);
            labelImgName.Name = "labelImgName";
            labelImgName.Size = new Size(85, 15);
            labelImgName.TabIndex = 8;
            labelImgName.Text = "labelImgName";
            labelImgName.Visible = false;
            // 
            // FormPersonaConfig
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(422, 442);
            Controls.Add(labelImgName);
            Controls.Add(buttonUploadImg);
            Controls.Add(pbPersonaImg);
            Controls.Add(buttonDeletePersona);
            Controls.Add(labelPersonaPrompt);
            Controls.Add(labelPersonaName);
            Controls.Add(buttonSavePersona);
            Controls.Add(richTextBoxPersonaPrompt);
            Controls.Add(textBoxPersonaName);
            FormBorderStyle = FormBorderStyle.FixedDialog;
            Name = "FormPersonaConfig";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Persona";
            ((System.ComponentModel.ISupportInitialize)pbPersonaImg).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox textBoxPersonaName;
        private RichTextBox richTextBoxPersonaPrompt;
        private Button buttonSavePersona;
        private Label labelPersonaName;
        private Label labelPersonaPrompt;
        private Button buttonDeletePersona;
        private PictureBox pbPersonaImg;
        private Button buttonUploadImg;
        private Label labelImgName;
    }
}
