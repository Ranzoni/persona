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
            SuspendLayout();
            // 
            // textBoxPersonaName
            // 
            textBoxPersonaName.Location = new Point(12, 26);
            textBoxPersonaName.Name = "textBoxPersonaName";
            textBoxPersonaName.Size = new Size(400, 23);
            textBoxPersonaName.TabIndex = 0;
            // 
            // richTextBoxPersonaPrompt
            // 
            richTextBoxPersonaPrompt.Location = new Point(12, 94);
            richTextBoxPersonaPrompt.Name = "richTextBoxPersonaPrompt";
            richTextBoxPersonaPrompt.Size = new Size(400, 193);
            richTextBoxPersonaPrompt.TabIndex = 1;
            richTextBoxPersonaPrompt.Text = "";
            // 
            // buttonSavePersona
            // 
            buttonSavePersona.Location = new Point(337, 293);
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
            labelPersonaName.Location = new Point(12, 9);
            labelPersonaName.Name = "labelPersonaName";
            labelPersonaName.Size = new Size(40, 15);
            labelPersonaName.TabIndex = 3;
            labelPersonaName.Text = "Nome";
            // 
            // labelPersonaPrompt
            // 
            labelPersonaPrompt.AutoSize = true;
            labelPersonaPrompt.Location = new Point(14, 76);
            labelPersonaPrompt.Name = "labelPersonaPrompt";
            labelPersonaPrompt.Size = new Size(47, 15);
            labelPersonaPrompt.TabIndex = 4;
            labelPersonaPrompt.Text = "Prompt";
            // 
            // buttonDeletePersona
            // 
            buttonDeletePersona.BackColor = SystemColors.Control;
            buttonDeletePersona.Image = Properties.Resources.trash;
            buttonDeletePersona.Location = new Point(12, 290);
            buttonDeletePersona.Name = "buttonDeletePersona";
            buttonDeletePersona.Size = new Size(30, 29);
            buttonDeletePersona.TabIndex = 5;
            buttonDeletePersona.UseVisualStyleBackColor = false;
            buttonDeletePersona.Visible = false;
            buttonDeletePersona.Click += buttonDeletePersona_Click;
            // 
            // FormPersonaConfig
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(422, 325);
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
    }
}
