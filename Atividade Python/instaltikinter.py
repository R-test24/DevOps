import customtkinter as ctk



# Configuração de aparência (opcional)

ctk.set_appearance_mode("Dark") # Modes: "System" (standard), "Dark", "Light"

ctk.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"



# 1. Criar a janela principal

app = ctk.CTk()

app.title("Minha Janela")

app.geometry("400x300")



# 2. Adicionar componentes (exemplo: Label)

label = ctk.CTkLabel(app, text="Olá, CustomTkinter!")

label.pack(pady=20)



# 3. Iniciar o loop

app.mainloop()




