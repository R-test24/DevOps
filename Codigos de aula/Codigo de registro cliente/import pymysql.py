import pymysql
conexao = pymysql.connect(
    host = "localhost",
    user = "admin",
    password = "1234",
    database = "empresa"
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
    
while True:
 
        print("\n===== MENU =====")
        print("1 - Consultar equipamentos")
        print("2 - Cadastrar equipamento")
        print("3 - Sair")
 
        opcao = input("Escolha: ")
 
        if opcao == "1":
 
            sql = "SELECT * FROM equipamentos"
            cursor.execute(sql)
 
            equipamentos = cursor.fetchall()
 
            print("\nLISTA DE EQUIPAMENTOS\n")
 
            for e in equipamentos:
                print(e)
 
        elif opcao == "2":
 
            nome = input("Nome: ")
            categoria = input("Categoria: ")
            patrimonio = input("Patrimônio: ")
            quantidade = int(input("Quantidade: "))
            localizacao = input("Localização: ")
            status = input("Status: ")
            data = input("Data (AAAA-MM-DD): ")
 
            sql = """
            INSERT INTO equipamentos
            (nome,categoria,patrimonio,quantidade,localizacao,status,data_cadastro)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
 
            valores = (
                nome,
                categoria,
                patrimonio,
                quantidade,
                localizacao,
                status,
                data
            )
 
            try:
                cursor.execute(sql, valores)
                conexao.commit()
                print("Equipamento cadastrado!")
 
            except Exception as erro:
                print("Sem permissão ou erro:", erro)
 
        elif opcao == "3":
            break
 
conexao.close()


    




    

    
  
    