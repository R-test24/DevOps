import tkinter as tk
from tkinter import ttk, messagebox

listaTeste = []
proximo_id = 1

class Estoque:
    def __init__(self, idItem, nomeItem, tipoItem, modeloItem, tamanhoItem,
                 marcaItem, quantidadeItem, fornecedorItem, precoCompra, precoVenda):
        
        self.idItem = idItem
        self.nomeItem = nomeItem
        self.tipoItem = tipoItem
        self.modeloItem = modeloItem
        self.tamanhoItem = tamanhoItem
        self.marcaItem = marcaItem
        self.quantidadeItem = quantidadeItem
        self.fornecedorItem = fornecedorItem
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda


# =========================
# FUNÇÕES
# =========================

def cadastrar_item():
    global proximo_id

    nome = entry_nome.get()
    tipo = combo_tipo.get()
    modelo = combo_modelo.get()
    tamanho = combo_tamanho.get()
    marca = entry_marca.get()

    try:
        quantidade = int(entry_quantidade.get())
        preco_compra = float(entry_preco_compra.get())
        preco_venda = float(entry_preco_venda.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preços devem ser numéricos.")
        return

    fornecedor = entry_fornecedor.get()

    if nome == "":
        messagebox.showwarning("Aviso", "Digite o nome do item.")
        return

    item = Estoque(
        proximo_id,
        nome,
        tipo,
        modelo,
        tamanho,
        marca,
        quantidade,
        fornecedor,
        preco_compra,
        preco_venda
    )

    listaTeste.append({
        "ID": item.idItem,
        "Nome": item.nomeItem,
        "Tipo": item.tipoItem,
        "Modelo": item.modeloItem,
        "Tamanho": item.tamanhoItem,
        "Marca": item.marcaItem,
        "Quantidade": item.quantidadeItem,
        "Fornecedor": item.fornecedorItem,
        "Preço Compra": item.precoCompra,
        "Preço Venda": item.precoVenda
    })

    tabela.insert("", "end", values=(
        item.idItem,
        item.nomeItem,
        item.tipoItem,
        item.modeloItem,
        item.tamanhoItem,
        item.marcaItem,
        item.quantidadeItem,
        item.fornecedorItem,
        f"R$ {item.precoCompra:.2f}",
        f"R$ {item.precoVenda:.2f}"
    ))

    proximo_id += 1

    limpar_campos()

    messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")


def limpar_campos():
    entry_nome.delete(0, tk.END)
    combo_tipo.set("")
    combo_modelo.set("")
    combo_tamanho.set("")
    entry_marca.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_fornecedor.delete(0, tk.END)
    entry_preco_compra.delete(0, tk.END)
    entry_preco_venda.delete(0, tk.END)


def consultar_item():
    nome_busca = entry_busca.get().lower()

    for item in tabela.get_children():
        tabela.delete(item)

    for item in listaTeste:
        if nome_busca in item["Nome"].lower():
            tabela.insert("", "end", values=(
                item["ID"],
                item["Nome"],
                item["Tipo"],
                item["Modelo"],
                item["Tamanho"],
                item["Marca"],
                item["Quantidade"],
                item["Fornecedor"],
                f"R$ {item['Preço Compra']:.2f}",
                f"R$ {item['Preço Venda']:.2f}"
            ))


def atualizar_modelo(event):
    tipo = combo_tipo.get()

    if tipo in ["Camiseta", "Regata"]:
        combo_modelo["values"] = ["Manga Curta", "Manga Longa"]
    else:
        combo_modelo.set("N/A")
        combo_modelo["values"] = ["N/A"]


# =========================
# JANELA PRINCIPAL
# =========================

janela = tk.Tk()
janela.title("Sistema de Estoque")
janela.geometry("1200x700")
janela.configure(bg="#f0f0f0")

titulo = tk.Label(
    janela,
    text="Sistema de Estoque",
    font=("Arial", 22, "bold"),
    bg="#f0f0f0"
)
titulo.pack(pady=10)

# =========================
# FRAME FORMULÁRIO
# =========================

frame_form = tk.Frame(janela, bg="#f0f0f0")
frame_form.pack(pady=10)

# Nome
tk.Label(frame_form, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1, padx=5)

# Tipo
tk.Label(frame_form, text="Tipo:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
combo_tipo = ttk.Combobox(
    frame_form,
    values=["Camiseta", "Calça", "Calção", "Regata"]
)
combo_tipo.grid(row=0, column=3, padx=5)
combo_tipo.bind("<<ComboboxSelected>>", atualizar_modelo)

# Modelo
tk.Label(frame_form, text="Modelo:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
combo_modelo = ttk.Combobox(frame_form)
combo_modelo.grid(row=0, column=5, padx=5)

# Tamanho
tk.Label(frame_form, text="Tamanho:", bg="#f0f0f0").grid(row=1, column=0, padx=5)
combo_tamanho = ttk.Combobox(
    frame_form,
    values=["P", "M", "G", "GG"]
)
combo_tamanho.grid(row=1, column=1, padx=5)

# Marca
tk.Label(frame_form, text="Marca:", bg="#f0f0f0").grid(row=1, column=2, padx=5)
entry_marca = tk.Entry(frame_form)
entry_marca.grid(row=1, column=3, padx=5)

# Quantidade
tk.Label(frame_form, text="Quantidade:", bg="#f0f0f0").grid(row=1, column=4, padx=5)
entry_quantidade = tk.Entry(frame_form)
entry_quantidade.grid(row=1, column=5, padx=5)

# Fornecedor
tk.Label(frame_form, text="Fornecedor:", bg="#f0f0f0").grid(row=2, column=0, padx=5)
entry_fornecedor = tk.Entry(frame_form)
entry_fornecedor.grid(row=2, column=1, padx=5)

# Preço Compra
tk.Label(frame_form, text="Preço Compra:", bg="#f0f0f0").grid(row=2, column=2, padx=5)
entry_preco_compra = tk.Entry(frame_form)
entry_preco_compra.grid(row=2, column=3, padx=5)

# Preço Venda
tk.Label(frame_form, text="Preço Venda:", bg="#f0f0f0").grid(row=2, column=4, padx=5)
entry_preco_venda = tk.Entry(frame_form)
entry_preco_venda.grid(row=2, column=5, padx=5)

# BOTÕES
frame_botoes = tk.Frame(janela, bg="#f0f0f0")
frame_botoes.pack(pady=10)

btn_cadastrar = tk.Button(
    frame_botoes,
    text="Cadastrar Item",
    bg="green",
    fg="white",
    width=20,
    command=cadastrar_item
)
btn_cadastrar.grid(row=0, column=0, padx=10)

btn_limpar = tk.Button(
    frame_botoes,
    text="Limpar",
    bg="gray",
    fg="white",
    width=20,
    command=limpar_campos
)
btn_limpar.grid(row=0, column=1, padx=10)

# BUSCA
frame_busca = tk.Frame(janela, bg="#f0f0f0")
frame_busca.pack(pady=10)

tk.Label(frame_busca, text="Buscar Item:", bg="#f0f0f0").grid(row=0, column=0, padx=5)

entry_busca = tk.Entry(frame_busca, width=30)
entry_busca.grid(row=0, column=1, padx=5)

btn_buscar = tk.Button(
    frame_busca,
    text="Consultar",
    command=consultar_item
)
btn_buscar.grid(row=0, column=2, padx=5)

# =========================
# TABELA
# =========================

colunas = (
    "ID",
    "Nome",
    "Tipo",
    "Modelo",
    "Tamanho",
    "Marca",
    "Quantidade",
    "Fornecedor",
    "Preço Compra",
    "Preço Venda"
)

tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=15)

for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=110)

tabela.pack(pady=20)

# =========================
# ITEM INICIAL
# =========================

item_inicial = Estoque(
    proximo_id,
    "Camiseta Opel",
    "Camiseta",
    "Manga Curta",
    "P",
    "Nike",
    10,
    "Fornecedor A",
    50.0,
    100.0
)

listaTeste.append({
    "ID": item_inicial.idItem,
    "Nome": item_inicial.nomeItem,
    "Tipo": item_inicial.tipoItem,
    "Modelo": item_inicial.modeloItem,
    "Tamanho": item_inicial.tamanhoItem,
    "Marca": item_inicial.marcaItem,
    "Quantidade": item_inicial.quantidadeItem,
    "Fornecedor": item_inicial.fornecedorItem,
    "Preço Compra": item_inicial.precoCompra,
    "Preço Venda": item_inicial.precoVenda
})

tabela.insert("", "end", values=(
    item_inicial.idItem,
    item_inicial.nomeItem,
    item_inicial.tipoItem,
    item_inicial.modeloItem,
    item_inicial.tamanhoItem,
    item_inicial.marcaItem,
    item_inicial.quantidadeItem,
    item_inicial.fornecedorItem,
    f"R$ {item_inicial.precoCompra:.2f}",
    f"R$ {item_inicial.precoVenda:.2f}"
))

proximo_id += 1

# =========================
# EXECUTAR
# =========================

janela.mainloop()