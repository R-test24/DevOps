import customtkinter as ctk

# Configuração
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("my_theme.json")

# Janela
app = ctk.CTk()
app.title("Login")
app.geometry("400x300")

# Título
titulo = ctk.CTkLabel(app, text="Sistema de Login", font=("Arial", 20))
titulo.pack(pady=20)

# Campo usuário
entry_usuario = ctk.CTkEntry(app, placeholder_text="Usuário")
entry_usuario.pack(pady=10)

# Campo senha
entry_senha = ctk.CTkEntry(app, placeholder_text="Senha", show="*")
entry_senha.pack(pady=10)

# Mensagem
mensagem = ctk.CTkLabel(app, text="")
mensagem.pack(pady=5)

# Função de login
def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "123":
        mensagem.configure(text="Login realizado com sucesso!", text_color="green")
    else:
        mensagem.configure(text="Usuário ou senha incorretos", text_color="red")

# Botão
botao_login = ctk.CTkButton(app, text="Entrar", command=fazer_login)
botao_login.pack(pady=15)

# Loop
app.mainloop()