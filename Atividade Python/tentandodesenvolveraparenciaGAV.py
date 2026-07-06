import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Estoque da GAV")
app.geometry("800x700")

# Aplicar cores diretamente (sem JSON)
label = ctk.CTkLabel(
    app, 
    text="Cadastro de Produtos!",
    text_color="#63382F",
    fg_color="transparent"
)
butao = ctk.CTkButton(app, text="Cadastrar", fg_color="#4ADE80", hover_color="#22C55E")
label.pack(pady=20)
butao.pack(pady=10)

app.mainloop()