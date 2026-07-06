import pymysql
conexao = pymysql.connect(
    host = "localhost",
    user = "administrador",
    password = "admin123",
    database = "controle_de_emprestimos"
)

cursor = conexao.cursor()
 
def cadastrar():
    try:
        nome = input("Digite seu nome: ")
        setor = input("Digite seu setor: ")
   
        sql = "INSERT INTO funcionarios (nome, setor) VALUES (%s, %s)"
        valores = (nome, setor)
   
        cursor.execute(sql, valores)
        conexao.commit()
        print("\nFuncionário cadastrado com sucesso!")
        
    except Exception as erro:
        print("\nERRO:", erro)
 
def listar():
    print("LISTA DE FUNCIONÁRIOS\n")
    sql = "SELECT * FROM funcionarios"
    cursor.execute(sql)
    resultado = cursor.fetchall()
 
    for C in resultado:
        print(f"ID: {C[0]}")
        print(f"Nome: {C[1]}")
        print(f"Setor: {C[2]}")
        print("-" * 30)
 
 
def excluir():
    id = input("Digite o ID do funcionário: ")
    sql = "DELETE FROM funcionarios WHERE id = %s"
    dados = (id,)
    cursor.execute(sql, dados)
    conexao.commit()
    print("Funcionário excluído com sucesso!")
   
 
def atualizar():
    id = input("Digite o ID do funcionário: ")
    telefone = input("Digite o novo telefone: ")
    endereco = input("Digite o novo endereco: ")
    sql = "UPDATE funcionarios SET telefone = %s, endereco = %s WHERE id = %s"
    dados = (telefone, endereco, id)
    cursor.execute(sql, dados)
    conexao.commit()
 
    print("Funcionário atualizado com sucesso!")
    
cadastrar()