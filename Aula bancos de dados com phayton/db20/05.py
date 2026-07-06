import pymysql
conexao = pymysql.connect(
    host= "localhost",
    user = "root",
    password = "root",
    database = "aula"    
)
cursor = conexao.cursor()

def cadastrar():
    nome = input("Digite seu nome:")
    telefone = input("Digite seu telefone:")
    email = input("Digite seu email:")
    cpf = input("Digite seu cpf:")
    endereco = input("Digite seu endereço:")
    
    sql = "INSERT INTO cliente (nome, telefone, email, cpf, endereco) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, telefone, email, cpf, endereco)
    
    cursor.execute(sql, valores)
    conexao.commit()
    print("CADASTRADOS COM SUESSO!")
    

    cadastrar()
            
def listar():
    sql = "SELECT * FROM cliente"
    cursor.execute(sql)
    resultado = cursor.fetchall()
    
    for c in resultado:     #percorra os dados dentro de resultados e armazene cada linha em c       
        print(f"Nome: {c[1]}")
        print(f"Telefone: {c[2]}")
        print(f"Email: {c[3]}")
        print(f"CPF: {c[4]}")
        print(f"Endereço: {c[5]}")
        print("-" * 30)
        


def excluir():
    id = input("Digite o ID do cliente: ")
    sql = "DELETE FROM cliente WHERE id = %s"
    dados = (id,)
    cursor.execute(sql,dados)
    conexao.commit()
    print("CLIENTE EXCLUÍDO COM SUCESSO!")
    


def atualizar():
    id = input("Digite o ID do cliente: ")
    novo_nome = input("Digite o novo nome do cliente: ")
    telefone = input("Digite o novo telefone do cliente: ") 
    email = input("Digite o novo email do cliente: ")
    sql = "UPDATE cliente SET nome = %s, telefone = %s, email = %s WHERE id = %s"
    dados = (novo_nome, telefone, email, id)
    cursor.execute(sql,dados)
    conexao.commit()
    print("CLIENTE ATUALIZADO COM SUCESSO!")
    
