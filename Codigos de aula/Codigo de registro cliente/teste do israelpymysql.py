import pymysql
 
conexao = pymysql.connect(
    host="localhost",
    user="professor",
    password="prof123",
    database="controle_de_emprestimos"
)
 
cursor = conexao.cursor()
 
def cadastrar():
    try:
        nome = input("Nome: ")
        categoria = input("Categoria: ")
        patrimonio = input("Patrimônio: ")
        quantidade = input("Quantidade: ")
        localizacao = input("Localização: ")
        status = input("Status: ")
        data_cadastro = input("Data de cadastro (YYYY-MM-DD): ")
 
        sql = "INSERT INTO equipamentos(nome,categoria,patrimonio,quantidade,localizacao,status,data_cadastro)VALUES (%s,%s,%s,%s,%s,%s,%s)"
        valores = (nome, categoria, patrimonio, quantidade, localizacao, status, data_cadastro)
 
        cursor.execute(sql, valores)
        conexao.commit()
        print("Equipamento cadastrado com sucesso!")
   
    except pymysql.Error as erro:
        print(f"Erro no banco de dados: {erro}")
 
    except ValueError:
        print("Quantidade deve ser um número inteiro!")
       
    except pymysql.Error as erro:
        print("Você não possui permissão para atualizar registros.")
        print(erro)
 
 
 
def listar():
    cursor.execute("SELECT * FROM equipamentos")
    dados = cursor.fetchall()
    print("\n=== EQUIPAMENTOS ===")
    for item in dados:
        print(item)
 
def atualizar():
    id_equipamento = int(input("ID do equipamento: "))
    novo_status = input("Novo status: ")
    nova_quantidade = int(input("Nova quantidade: "))
 
    sql = "UPDATE equipamentos SET status=%s, quantidade=%s WHERE id_equipamento=%s"
 
    valores = (novo_status, nova_quantidade, id_equipamento)
 
    cursor.execute(sql, valores)
    conexao.commit()
 
    print("Equipamento atualizado!")
 
def excluir():
    id_equipamento = int(input("ID do equipamento: "))
 
    sql = "DELETE FROM equipamentos WHERE id_equipamento=%s"
 
    cursor.execute(sql, (id_equipamento,))
    conexao.commit()
 
    print("Equipamento excluído!")
 
while True:
 
    print("\n===== SISTEMA DE EQUIPAMENTOS =====")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Atualizar")
    print("4 - Excluir")
    print("5 - Sair")
 
    opcao = input("Escolha: ")
 
    if opcao == "1":
        cadastrar()
    elif opcao == "2":
        listar()
    elif opcao == "3":
        atualizar()
    elif opcao == "4":
        excluir()
    elif opcao == "5":
        print("Sistema encerrado.")
        break
    else:
        print("Opção inválida!")
 
cursor.close()
conexao.close()