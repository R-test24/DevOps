
def cadastrar(): 

    nome   = entry_nome.get() 
    cpf    = entry_cpf.get() 
    email  = entry_email.get() 
    cidade = entry_cidade.get() 

    if len(nome) == 0: 

        mostrar_msg("Nome não pode estar em branco!", "erro") 

        return 

    if len(cpf) != 11 or not cpf.isdigit(): 

        mostrar_msg(f"CPF inválido! Digitou {len(cpf)} caracteres.", "erro") 

        return 

    if "@" not in email: 

        mostrar_msg("E-mail inválido! Precisa ter @.", "erro") 

        return 

    if len(cidade) == 0: 

        mostrar_msg("Cidade não pode estar em branco!", "erro") 

        return 

 

    cliente = { 

        "nome":   nome, 

        "cpf":    cpf, 

        "email":  email, 

        "cidade": cidade 

    } 

    clientes.append(cliente) 

    mostrar_msg(f"Cliente '{nome}' cadastrado! Total: {len(clientes)}", "ok") 
    

    limpar_campos() 

    atualizar_lista() 


def buscar(): 

    cpf_busca = entry_busca.get() 

 

    if len(cpf_busca) == 0: 

        mostrar_msg("Digite um CPF para buscar.", "erro") 

        return 

 

    for cliente in clientes: 

        if cliente["cpf"] == cpf_busca: 

            resultado = ( 

                f"Cliente encontrado!\n\n" 

                f"Nome:   {cliente['nome']}\n" 

                f"CPF:    {cliente['cpf']}\n" 


                f"E-mail: {cliente['email']}\n" 

                f"Cidade: {cliente['cidade']}" 

            ) 

            mostrar_msg(resultado, "ok") 

            return 

 

    mostrar_msg(f"CPF {cpf_busca} não encontrado.", "erro") 


def atualizar_lista(): 

    txt_lista.configure(state="normal") 

    txt_lista.delete("1.0", ctk.END) 

 

    if len(clientes) == 0: 

        txt_lista.insert("1.0", "Nenhum cliente cadastrado ainda.") 

    else: 

        for i, c in enumerate(clientes): 

            linha = f"{i+1}. {c['nome']} | CPF: {c['cpf']} | {c['cidade']}\n" 

            txt_lista.insert(ctk.END, linha) 

 

    txt_lista.configure(state="disabled") 


def limpar_campos(): 

    entry_nome.delete(0, ctk.END) 

    entry_cpf.delete(0, ctk.END) 

    entry_email.delete(0, ctk.END) 

    entry_cidade.delete(0, ctk.END) 

    entry_nome.focus() 

 

def mostrar_msg(texto, tipo): 

    cor = "#4ade80" if tipo == "ok" else "#f87171" 

    label_msg.configure(text=texto, text_color=cor) 


app = ctk.CTk() 

app.title("InfoStart — Cadastro de Clientes") 

app.geometry("520x720") 

app.resizable(False, False) 


ctk.CTkLabel(app, text="InfoStart", font=("Arial", 26, "bold")).pack(pady=(20, 2)) 

ctk.CTkLabel(app, text="Cadastro de Clientes", text_color="gray").pack(pady=(0, 10)) 

 

tabview = ctk.CTkTabview(app, height=360) 

tabview.pack(fill="x", padx=20, pady=10) 

 

aba_cad  = tabview.add("Cadastrar") 

aba_list = tabview.add("Listar") 

aba_bus  = tabview.add("Buscar por CPF") 


ctk.CTkLabel(aba_cad, text="Nome completo", anchor="w").pack(fill="x", padx=10) 

entry_nome = ctk.CTkEntry(aba_cad, placeholder_text="Ex: João Silva", height=36) 

entry_nome.pack(fill="x", padx=10, pady=(2, 8)) 

 # ERRO AQUI

# (mesma estrutura para CPF, E-mail e Cidade) 

 

frame_btn = ctk.CTkFrame(aba_cad, fg_color="transparent") 

frame_btn.pack(fill="x", padx=10) 

 

ctk.CTkButton(frame_btn, text="Cadastrar", height=40, 

              font=("Arial", 13, "bold"), command=cadastrar).pack( 

              side="left", expand=True, fill="x", padx=(0, 5)) 

 

ctk.CTkButton(frame_btn, text="Limpar", height=40, 

              fg_color="gray30", hover_color="gray40", 

              command=limpar_campos).pack( 

              side="left", expand=True, fill="x", padx=(5, 0)) 


txt_lista = ctk.CTkTextbox(aba_list, height=240, font=("Courier New", 13)) 

txt_lista.pack(fill="x", padx=10, pady=(0, 10)) 

txt_lista.insert("1.0", "Nenhum cliente cadastrado ainda.") 

txt_lista.configure(state="disabled") 

 

ctk.CTkButton(aba_list, text="Atualizar Lista", height=36, 

              command=atualizar_lista).pack(fill="x", padx=10, pady=(0, 10)) 


ctk.CTkLabel(aba_bus, text="Digite o CPF para buscar:", anchor="w").pack( 

    fill="x", padx=10, pady=(20, 4)) 

 

entry_busca = ctk.CTkEntry(aba_bus, placeholder_text="Ex: 12345678900", height=36) 

entry_busca.pack(fill="x", padx=10, pady=(0, 10)) 

 

ctk.CTkButton(aba_bus, text="Buscar", height=40, 

              font=("Arial", 13, "bold"), command=buscar).pack(fill="x", padx=10) 


label_msg = ctk.CTkLabel( 

    app, text="", font=("Arial", 13), 

    justify="left", anchor="w", wraplength=480 

) 

label_msg.pack(padx=20, pady=10, fill="x") 

 

ctk.CTkLabel(app, text="Sistema InfoStart  ·  Jovem Programador 2026  ·  SENAC SC", 

             text_color="gray", font=("Arial", 11)).pack(side="bottom", pady=10) 

 

app.mainloop() 






    
    

