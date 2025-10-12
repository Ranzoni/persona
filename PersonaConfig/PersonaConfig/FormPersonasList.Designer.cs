namespace PersonaConfig
{
    partial class FormPersonasList
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            comboBoxPersonas = new ComboBox();
            labelPersonas = new Label();
            buttonUpdatePersona = new Button();
            buttonAddPersona = new Button();
            SuspendLayout();
            // 
            // comboBoxPersonas
            // 
            comboBoxPersonas.DropDownStyle = ComboBoxStyle.DropDownList;
            comboBoxPersonas.FormattingEnabled = true;
            comboBoxPersonas.Location = new Point(12, 27);
            comboBoxPersonas.Name = "comboBoxPersonas";
            comboBoxPersonas.Size = new Size(317, 23);
            comboBoxPersonas.TabIndex = 0;
            // 
            // labelPersonas
            // 
            labelPersonas.AutoSize = true;
            labelPersonas.Location = new Point(12, 9);
            labelPersonas.Name = "labelPersonas";
            labelPersonas.Size = new Size(54, 15);
            labelPersonas.TabIndex = 1;
            labelPersonas.Text = "Personas";
            // 
            // buttonUpdatePersona
            // 
            buttonUpdatePersona.Location = new Point(335, 26);
            buttonUpdatePersona.Name = "buttonUpdatePersona";
            buttonUpdatePersona.Size = new Size(75, 23);
            buttonUpdatePersona.TabIndex = 2;
            buttonUpdatePersona.Text = "Alterar";
            buttonUpdatePersona.UseVisualStyleBackColor = true;
            buttonUpdatePersona.Click += buttonUpdatePersona_Click;
            // 
            // buttonAddPersona
            // 
            buttonAddPersona.Location = new Point(12, 67);
            buttonAddPersona.Name = "buttonAddPersona";
            buttonAddPersona.Size = new Size(108, 23);
            buttonAddPersona.TabIndex = 3;
            buttonAddPersona.Text = "+ Criar um novo";
            buttonAddPersona.UseVisualStyleBackColor = true;
            buttonAddPersona.Click += buttonAddPersona_Click;
            // 
            // FormPersonasList
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(422, 103);
            Controls.Add(buttonAddPersona);
            Controls.Add(buttonUpdatePersona);
            Controls.Add(labelPersonas);
            Controls.Add(comboBoxPersonas);
            FormBorderStyle = FormBorderStyle.FixedDialog;
            Name = "FormPersonasList";
            Text = "Persona";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ComboBox comboBoxPersonas;
        private Label labelPersonas;
        private Button buttonUpdatePersona;
        private Button buttonAddPersona;
    }
}