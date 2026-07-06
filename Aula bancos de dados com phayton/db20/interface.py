import customtkinter as ctk
from tkinter import ttk
import mysql.connector

# ===================== CONFIG =====================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ===================== APP =====================
app = ctk.CTk()
app.title("ERP - Sistema de Estoque")
app.geometry("1200x700")

# ===================== BANCO =====================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="loja"
    )

# ===================== FUNÇÃO SALVAR =====================
def salvar():
    nome = entry_nome.get()
    tipo = entry_tipo.get()
    preco = entry_preco.get()

    if nome == "" or tipo == "" or preco == "":
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO produtos (nome, tipo, preco) VALUES (%s, %s, %s)",
        (nome, tipo, preco)
    )

    conexao.commit()

    tabela.insert("", "end", values=(nome, tipo, preco))

    entry_nome.delete(0, "end")
    entry_tipo.delete(0, "end")
    entry_preco.delete(0, "end")

# ===================== SIDEBAR =====================
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(
    sidebar,
    text="⚡ GAV ERP",
    font=("Arial", 22, "bold")
).pack(pady=30)

ctk.CTkButton(sidebar, text="📦 Produtos").pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="👥 Clientes").pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="💰 Vendas").pack(pady=10, padx=20)

# ===================== MAIN AREA =====================
main = ctk.CTkFrame(app)
main.pack(side="right", expand=True, fill="both", padx=15, pady=15)

# ===================== TOP BAR =====================
topbar = ctk.CTkFrame(main, height=60)
topbar.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(
    topbar,
    text="Painel de Produtos",
    font=("Arial", 20, "bold")
).pack(side="left", padx=20)

# ===================== CARDS =====================
cards_frame = ctk.CTkFrame(main)
cards_frame.pack(fill="x", padx=10)

card1 = ctk.CTkFrame(cards_frame, width=200, height=80)
card1.pack(side="left", padx=10, pady=10)

ctk.CTkLabel(card1, text="Total Produtos", font=("Arial", 14)).pack(pady=5)
ctk.CTkLabel(card1, text="--", font=("Arial", 18, "bold")).pack()

# ===================== FORM =====================
form = ctk.CTkFrame(main)
form.pack(fill="x", padx=10, pady=10)

entry_nome = ctk.CTkEntry(form, placeholder_text="Nome do produto", width=250)
entry_nome.grid(row=0, column=0, padx=10, pady=10)

entry_tipo = ctk.CTkEntry(form, placeholder_text="Tipo", width=250)
entry_tipo.grid(row=0, column=1, padx=10, pady=10)

entry_preco = ctk.CTkEntry(form, placeholder_text="Preço", width=250)
entry_preco.grid(row=0, column=2, padx=10, pady=10)

btn = ctk.CTkButton(form, text="Salvar", command=salvar)
btn.grid(row=0, column=3, padx=10)

# ===================== TABELA =====================
table_frame = ctk.CTkFrame(main)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="#1e1e1e",
    foreground="white",
    rowheight=30,
    fieldbackground="#1e1e1e"
)

style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

colunas = ("Nome", "Tipo", "Preço")

tabela = ttk.Treeview(table_frame, columns=colunas, show="headings")

for c in colunas:
    tabela.heading(c, text=c)
    tabela.column(c, width=200)

tabela.pack(fill="both", expand=True)

# ===================== START =====================
app.mainloop()