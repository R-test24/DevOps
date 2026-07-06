import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Loja de Roupas - Sistema de Estoque")
app.geometry("850x650")

# =========================
# DADOS
# =========================
estoque = []

# =========================
# MENU
# =========================
menu = ctk.CTkFrame(app, width=180, corner_radius=0)
menu.pack(side="left", fill="y")

ctk.CTkLabel(menu, text="LOJA", font=("Arial", 18)).pack(pady=20)

# =========================
# TELAS
# =========================
frame_estoque = ctk.CTkFrame(app)
frame_vendas = ctk.CTkFrame(app)

def abrir_estoque():
    frame_vendas.pack_forget()
    frame_estoque.pack(fill="both", expand=True)

def abrir_vendas():
    frame_estoque.pack_forget()
    frame_vendas.pack(fill="both", expand=True)

ctk.CTkButton(menu, text="Estoque", command=abrir_estoque).pack(pady=10)
ctk.CTkButton(menu, text="Vendas", command=abrir_vendas).pack(pady=10)

# =========================
# ESTOQUE
# =========================
ctk.CTkLabel(frame_estoque, text="Controle de Estoque", font=("Arial", 22)).pack(pady=10)

entry_nome = ctk.CTkEntry(frame_estoque, placeholder_text="Nome da peça")
entry_nome.pack(pady=5)

entry_tam = ctk.CTkEntry(frame_estoque, placeholder_text="Tamanho (P/M/G)")
entry_tam.pack(pady=5)

entry_qtd = ctk.CTkEntry(frame_estoque, placeholder_text="Quantidade")
entry_qtd.pack(pady=5)

lista_estoque = ctk.CTkTextbox(frame_estoque, width=450, height=250)
lista_estoque.pack(pady=10)

def atualizar_estoque():
    lista_estoque.delete("0.0", "end")
    for i, p in enumerate(estoque):
        lista_estoque.insert(
            "end",
            f"{i+1}. {p['nome']} | Tam: {p['tam']} | Qtd: {p['qtd']}\n"
        )

def adicionar_produto():
    nome = entry_nome.get()
    tam = entry_tam.get()
    qtd = entry_qtd.get()

    if nome and tam and qtd:
        estoque.append({
            "nome": nome,
            "tam": tam,
            "qtd": int(qtd)
        })
        atualizar_estoque()

        entry_nome.delete(0, "end")
        entry_tam.delete(0, "end")
        entry_qtd.delete(0, "end")

ctk.CTkButton(frame_estoque, text="Adicionar produto", command=adicionar_produto).pack(pady=5)

# =========================
# VENDAS (COM TAMANHO)
# =========================
ctk.CTkLabel(frame_vendas, text="Registro de Vendas", font=("Arial", 22)).pack(pady=10)

entry_venda_nome = ctk.CTkEntry(frame_vendas, placeholder_text="Nome da peça")
entry_venda_nome.pack(pady=5)

entry_venda_tam = ctk.CTkEntry(frame_vendas, placeholder_text="Tamanho (P/M/G)")
entry_venda_tam.pack(pady=5)

entry_venda_qtd = ctk.CTkEntry(frame_vendas, placeholder_text="Quantidade vendida")
entry_venda_qtd.pack(pady=5)

msg_venda = ctk.CTkLabel(frame_vendas, text="")
msg_venda.pack(pady=5)

def registrar_venda():
    nome = entry_venda_nome.get()
    tam = entry_venda_tam.get()
    qtd = entry_venda_qtd.get()

    if not nome or not tam or not qtd:
        msg_venda.configure(text="Preencha todos os campos!", text_color="orange")
        return

    qtd = int(qtd)

    for produto in estoque:
        if (
            produto["nome"].lower() == nome.lower()
            and produto["tam"].lower() == tam.lower()
        ):

            if produto["qtd"] >= qtd:
                produto["qtd"] -= qtd
                msg_venda.configure(text="Venda registrada com sucesso!", text_color="green")
                atualizar_estoque()
            else:
                msg_venda.configure(text="Estoque insuficiente!", text_color="red")
            return

    msg_venda.configure(text="Produto não encontrado!", text_color="red")

ctk.CTkButton(frame_vendas, text="Registrar venda", command=registrar_venda).pack(pady=10)

# =========================
# INÍCIO
# =========================
abrir_estoque()

app.mainloop()