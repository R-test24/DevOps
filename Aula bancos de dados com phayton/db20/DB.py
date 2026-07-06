import mysql.connector

conexao = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "root",
    database= "aula"
    
)

cursor = conexao.cursor()

def cadatrar():
    nome = input("Digite seu nome:")
    telefone = input("Digite seu telefone:")
    email = input("Digite seu email:")
    cpf = input("Digite seu cpf:")
    endereco = input("Digite seu endereço:")
    
    sql = "INSERT INTO clientes (nome, telefone, email, cpf, endereco) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, telefone, email, cpf, endereco)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Cadastro realizado com sucesso!")
    