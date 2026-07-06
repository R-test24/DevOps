import customtkinter as ctk
from tkinter import ttk, messagebox
import pymysql

# ======================
# CONEXÃO
# ======================
conexao = pymysql.connect(
    host="localhost",
    user="admin",
    password="1234",
    database="empresa"
)

cursor = conexao.cursor()

# ======================
# JANELA
# ======================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.geometry("1100x650")
janela.title("ERP Empresa")

# ======================
# LOGIN FUNCTION
# ======================
def fazer_login():
    usuario = entry_user.get()
    senha = entry_pass.get()

    sql = "SELECT * FROM usuarios WHERE usuario=%s AND senha=%s"
    cursor.execute(sql, (usuario, senha))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Sucesso", "Login realizado!")

        frame_login.pack_forget()
        frame_principal.pack(fill="both", expand=True)

        listar()

    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# ======================
# FRAME LOGIN
# ======================
frame_login = ctk.CTkFrame(janela)
frame_login.pack(fill="both", expand=True)

ctk.CTkLabel(
    frame_login,
    text="LOGIN DO SISTEMA",
    font=("Arial", 28, "bold")
).pack(pady=40)

entry_user = ctk.CTkEntry(frame_login, placeholder_text="admin")
entry_user.pack(pady=10)

entry_pass = ctk.CTkEntry(frame_login, placeholder_text="1234", show="*")
entry_pass.pack(pady=10)

ctk.CTkButton(
    frame_login,
    text="Entrar",
    command=fazer_login
).pack(pady=20)

# ======================
# FUNÇÕES DO SISTEMA
# ======================
def cadastrar():
    nome = entry_nome.get()
    setor = entry_setor.get()

    sql = "INSERT INTO funcionarios (nome, setor) VALUES (%s, %s)"
    cursor.execute(sql, (nome, setor))
    conexao.commit()
    listar()

def listar():
    tabela.delete(*tabela.get_children())

    cursor.execute("SELECT * FROM funcionarios")
    for i in cursor.fetchall():
        tabela.insert("", "end", values=i)

def excluir():
    item = tabela.selection()[0]
    id_func = tabela.item(item, "values")[0]

    cursor.execute("DELETE FROM funcionarios WHERE id=%s", (id_func,))
    conexao.commit()
    listar()

def atualizar():
    id_func = entry_id.get()
    nome = entry_nome.get()
    setor = entry_setor.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    sql = """
    UPDATE funcionarios
    SET nome=%s, setor=%s, telefone=%s, endereco=%s
    WHERE id=%s
    """

    cursor.execute(sql, (nome, setor, telefone, endereco, id_func))
    conexao.commit()
    listar()

# ======================
# FRAME PRINCIPAL (ERP)
# ======================
frame_principal = ctk.CTkFrame(janela)

titulo = ctk.CTkLabel(
    frame_principal,
    text="Sistema de Funcionários",
    font=("Arial", 26, "bold")
)
titulo.pack(pady=20)

entry_id = ctk.CTkEntry(frame_principal, placeholder_text="ID")
entry_id.pack(pady=5)

entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Nome")
entry_nome.pack(pady=5)

entry_setor = ctk.CTkEntry(frame_principal, placeholder_text="Setor")
entry_setor.pack(pady=5)

entry_telefone = ctk.CTkEntry(frame_principal, placeholder_text="Telefone")
entry_telefone.pack(pady=5)

entry_endereco = ctk.CTkEntry(frame_principal, placeholder_text="Endereço")
entry_endereco.pack(pady=5)

ctk.CTkButton(frame_principal, text="Cadastrar", command=cadastrar).pack(pady=5)
ctk.CTkButton(frame_principal, text="Atualizar", command=atualizar).pack(pady=5)
ctk.CTkButton(frame_principal, text="Excluir", command=excluir).pack(pady=5)

# TABELA
frame_table = ctk.CTkFrame(frame_principal)
frame_table.pack(fill="both", expand=True, pady=10)

colunas = ("ID", "Nome", "Setor", "Telefone", "Endereco")

tabela = ttk.Treeview(frame_table, columns=colunas, show="headings")

for c in colunas:
    tabela.heading(c, text=c)
    tabela.column(c, width=150)

tabela.pack(fill="both", expand=True)

# INICIA NO LOGIN
janela.mainloop()