import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# =========================
# CONEXÃO MYSQL
# =========================
conexao = pymysql.connect(
    host="localhost",
    user="admin",
    password="1234",
    database="emprestimo"
)

cursor = conexao.cursor()

# =========================
# FUNÇÕES
# =========================

def cadastrar():
    try:
        sql = """
        INSERT INTO equipamentos
        (nome,categoria,patrimonio,quantidade,localizacao,status,data_cadastro)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (
            txt_nome.get(),
            txt_categoria.get(),
            txt_patrimonio.get(),
            txt_quantidade.get(),
            txt_localizacao.get(),
            txt_status.get(),
            txt_data.get()
        )

        cursor.execute(sql, valores)
        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Equipamento cadastrado!"
        )

        limpar()
        listar()

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            str(erro)
        )

def listar():

    tabela.delete(*tabela.get_children())

    cursor.execute("SELECT * FROM equipamentos")

    dados = cursor.fetchall()

    for item in dados:
        tabela.insert("", tk.END, values=item)


def atualizar():

    try:
        item = tabela.focus()

        dados = tabela.item(item)

        id_equipamento = dados["values"][0]

        sql = """
        UPDATE equipamentos
        SET status=%s,
            quantidade=%s
        WHERE id_equipamento=%s
        """

        valores = (
            txt_status.get(),
            txt_quantidade.get(),
            id_equipamento
        )

        cursor.execute(sql, valores)
        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Equipamento atualizado!"
        )

        listar()

    except:
        messagebox.showwarning(
            "Aviso",
            "Selecione um equipamento!"
        )


def excluir():

    try:

        item = tabela.focus()

        dados = tabela.item(item)

        id_equipamento = dados["values"][0]

        sql = "DELETE FROM equipamentos WHERE id_equipamento=%s"

        cursor.execute(sql, (id_equipamento,))
        conexao.commit()

        listar()

        messagebox.showinfo(
            "Sucesso",
            "Equipamento removido!"
        )

    except:
        messagebox.showwarning(
            "Aviso",
            "Selecione um registro!"
        )


def selecionar(event):

    item = tabela.focus()

    dados = tabela.item(item)

    valores = dados["values"]

    if valores:

        txt_nome.delete(0, tk.END)
        txt_categoria.delete(0, tk.END)
        txt_patrimonio.delete(0, tk.END)
        txt_quantidade.delete(0, tk.END)
        txt_localizacao.delete(0, tk.END)
        txt_status.delete(0, tk.END)
        txt_data.delete(0, tk.END)

        txt_nome.insert(0, valores[1])
        txt_categoria.insert(0, valores[2])
        txt_patrimonio.insert(0, valores[3])
        txt_quantidade.insert(0, valores[4])
        txt_localizacao.insert(0, valores[5])
        txt_status.insert(0, valores[6])
        txt_data.insert(0, valores[7])


def limpar():

    txt_nome.delete(0, tk.END)
    txt_categoria.delete(0, tk.END)
    txt_patrimonio.delete(0, tk.END)
    txt_quantidade.delete(0, tk.END)
    txt_localizacao.delete(0, tk.END)
    txt_status.delete(0, tk.END)
    txt_data.delete(0, tk.END)

# =========================
# JANELA
# =========================

janela = tk.Tk()
janela.title("ERP Equipamentos")
janela.geometry("1300x700")
janela.configure(bg="#111827")

# =========================
# ESTILO
# =========================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1F2937",
    foreground="white",
    fieldbackground="#1F2937",
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    background="#2563EB",
    foreground="white",
    font=("Segoe UI", 10, "bold")
)

# =========================
# MENU LATERAL
# =========================

menu = tk.Frame(
    janela,
    bg="#0F172A",
    width=220
)

menu.pack(side="left", fill="y")

titulo = tk.Label(
    menu,
    text="ERP",
    fg="white",
    bg="#0F172A",
    font=("Segoe UI", 24, "bold")
)

titulo.pack(pady=30)

btn_cadastrar = tk.Button(
    menu,
    text="Cadastrar",
    bg="#2563EB",
    fg="white",
    font=("Segoe UI", 11),
    command=cadastrar
)

btn_cadastrar.pack(fill="x", padx=15, pady=5)

btn_atualizar = tk.Button(
    menu,
    text="Atualizar",
    bg="#10B981",
    fg="white",
    font=("Segoe UI", 11),
    command=atualizar
)

btn_atualizar.pack(fill="x", padx=15, pady=5)

btn_excluir = tk.Button(
    menu,
    text="Excluir",
    bg="#EF4444",
    fg="white",
    font=("Segoe UI", 11),
    command=excluir
)

btn_excluir.pack(fill="x", padx=15, pady=5)

# =========================
# ÁREA PRINCIPAL
# =========================

conteudo = tk.Frame(
    janela,
    bg="#111827"
)

conteudo.pack(
    side="right",
    fill="both",
    expand=True
)

# =========================
# FORMULÁRIO
# =========================

frame_form = tk.LabelFrame(
    conteudo,
    text="Cadastro de Equipamentos",
    bg="#111827",
    fg="white"
)

frame_form.pack(
    fill="x",
    padx=15,
    pady=15
)

campos = [
    "Nome",
    "Categoria",
    "Patrimônio",
    "Quantidade",
    "Localização",
    "Status",
    "Data"
]

entries = []

for i, campo in enumerate(campos):

    tk.Label(
        frame_form,
        text=campo,
        bg="#111827",
        fg="white"
    ).grid(row=i//4*2, column=i%4, padx=10)

    e = tk.Entry(
        frame_form,
        width=25
    )

    e.grid(
        row=i//4*2+1,
        column=i%4,
        padx=10,
        pady=5
    )

    entries.append(e)

(
txt_nome,
txt_categoria,
txt_patrimonio,
txt_quantidade,
txt_localizacao,
txt_status,
txt_data
) = entries

# =========================
# TABELA
# =========================

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

tabela = ttk.Treeview(
    conteudo,
    columns=colunas,
    show="headings"
)

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, anchor="center")

tabela.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

tabela.bind(
    "<<TreeviewSelect>>",
    selecionar
)

listar()

janela.mainloop()

cursor.close()
conexao.close()