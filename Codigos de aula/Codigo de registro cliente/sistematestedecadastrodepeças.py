import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
 
# CONEXÃO COM O BANCO
conexao = pymysql.connect(
    host="localhost",
    user="administrador",
    password="admin123",
    database="controle_de_emprestimo"
)
 
cursor = conexao.cursor()
 
# ================= FUNÇÕES =================
 
def cadastrar():
    try:
        sql = """
        INSERT INTO equipamentos
        (nome, categoria, patrimonio, quantidade, localizacao, status, data_cadastro)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
 
        valores = (
            entry_nome.get(),
            entry_categoria.get(),
            entry_patrimonio.get(),
            entry_quantidade.get(),
            entry_localizacao.get(),
            entry_status.get(),
            entry_data.get()
        )
 
        cursor.execute(sql, valores)
        conexao.commit()
 
        messagebox.showinfo("Sucesso", "Equipamento cadastrado!")
 
        limpar_campos()
        listar()
 
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))

def listar():
    tabela.delete(*tabela.get_children())
 
    cursor.execute("SELECT * FROM equipamentos")
    dados = cursor.fetchall()
 
    for linha in dados:
        tabela.insert("", tk.END, values=linha)
 
 
def atualizar():
    try:
        sql = """
        UPDATE equipamentos
        SET status=%s, quantidade=%s
        WHERE id_equipamento=%s
        """
 
        cursor.execute(
            sql,
            (
                entry_status.get(),
                entry_quantidade.get(),
                entry_id.get()
            )
        )
 
        conexao.commit()
 
        messagebox.showinfo("Sucesso", "Equipamento atualizado!")
        listar()
 
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))
 
 
def excluir():
    try:
        sql = "DELETE FROM equipamentos WHERE id_equipamento=%s"
 
        cursor.execute(sql, (entry_id.get(),))
        conexao.commit()
 
        messagebox.showinfo("Sucesso", "Equipamento excluído!")
        listar()
 
    except Exception as erro:
        messagebox.showerror("Erro", str(erro))
 
 
def selecionar(event):
    item = tabela.focus()
 
    if item:
        valores = tabela.item(item, "values")
 
        entry_id.delete(0, tk.END)
        entry_id.insert(0, valores[0])
 
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])
 
        entry_categoria.delete(0, tk.END)
        entry_categoria.insert(0, valores[2])
 
        entry_patrimonio.delete(0, tk.END)
        entry_patrimonio.insert(0, valores[3])
 
        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(0, valores[4])
 
        entry_localizacao.delete(0, tk.END)
        entry_localizacao.insert(0, valores[5])
 
        entry_status.delete(0, tk.END)
        entry_status.insert(0, valores[6])
 
        entry_data.delete(0, tk.END)
        entry_data.insert(0, valores[7])
 
 
def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_patrimonio.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_localizacao.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    

def validar_campos():
    if entry_nome.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Nome.")
        entry_nome.focus()
        return False

    if entry_categoria.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Categoria.")
        entry_categoria.focus()
        return False

    if entry_patrimonio.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Patrimônio.")
        entry_patrimonio.focus()
        return False

    if entry_quantidade.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Quantidade.")
        entry_quantidade.focus()
        return False

    if entry_localizacao.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Localização.")
        entry_localizacao.focus()
        return False

    if entry_status.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Status.")
        entry_status.focus()
        return False

    if entry_data.get().strip() == "":
        messagebox.showwarning("Campo vazio", "Preencha o campo Data Cadastro.")
        entry_data.focus()
        return False

    return True

def validar_campos():
    campos = [
        (entry_nome, "Nome"),
        (entry_categoria, "Categoria"),
        (entry_patrimonio, "Patrimônio"),
        (entry_quantidade, "Quantidade"),
        (entry_localizacao, "Localização"),
        (entry_status, "Status"),
        (entry_data, "Data Cadastro")
    ]

    for campo, nome in campos:
        campo.config(bg="white")

    for campo, nome in campos:
        if campo.get().strip() == "":
            campo.config(bg="#ffcccc")
            campo.focus()
            messagebox.showwarning(
                "Campo obrigatório",
                f"O campo '{nome}' deve ser preenchido."
            )
            return False

    return True


 
# ================= JANELA =================
 
janela = tk.Tk()
janela.title("Sistema de Controle de Equipamentos")
janela.geometry("1100x600")
 
# CAMPOS
 
tk.Label(janela, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(janela)
entry_id.grid(row=0, column=1)
 
tk.Label(janela, text="Nome").grid(row=1, column=0)
entry_nome = tk.Entry(janela, width=40)
entry_nome.grid(row=1, column=1)
 
tk.Label(janela, text="Categoria").grid(row=2, column=0)
entry_categoria = tk.Entry(janela, width=40)
entry_categoria.grid(row=2, column=1)
 
tk.Label(janela, text="Patrimônio").grid(row=3, column=0)
entry_patrimonio = tk.Entry(janela, width=40)
entry_patrimonio.grid(row=3, column=1)
 
tk.Label(janela, text="Quantidade").grid(row=4, column=0)
entry_quantidade = tk.Entry(janela, width=40)
entry_quantidade.grid(row=4, column=1)
 
tk.Label(janela, text="Localização").grid(row=5, column=0)
entry_localizacao = tk.Entry(janela, width=40)
entry_localizacao.grid(row=5, column=1)
 
tk.Label(janela, text="Status").grid(row=6, column=0)
entry_status = tk.Entry(janela, width=40)
entry_status.grid(row=6, column=1)
 
tk.Label(janela, text="Data Cadastro").grid(row=7, column=0)
entry_data = tk.Entry(janela, width=40)
entry_data.grid(row=7, column=1)
 
# BOTÕES
 
tk.Button(janela, text="Cadastrar", bg="green", fg="white",
          command=cadastrar).grid(row=8, column=0, pady=10)
 
tk.Button(janela, text="Atualizar", bg="orange", fg="white",
          command=atualizar).grid(row=8, column=1)
 
tk.Button(janela, text="Excluir", bg="red", fg="white",
          command=excluir).grid(row=8, column=2)
 
tk.Button(janela, text="Listar",
          command=listar).grid(row=8, column=3)
 
# TABELA
 
colunas = (
    "ID",
    "Nome",
    "Categoria",
    "Patrimônio",
    "Quantidade",
    "Localização",
    "Status",
    "Data"
)
 
tabela = ttk.Treeview(janela, columns=colunas, show="headings")
 
for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=120)
 
tabela.grid(row=10, column=0, columnspan=8, padx=10, pady=20)
 
tabela.bind("<<TreeviewSelect>>", selecionar)
 
listar()
 
janela.mainloop()
 
cursor.close()
conexao.close()