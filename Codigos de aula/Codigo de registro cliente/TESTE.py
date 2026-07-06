import pymysql
conexao = pymysql.connect(
    host = "localhost",
    user = "administrador",
    password = "admin123",
    database = "controle_de_emprestimos"
)
cursor = conexao.cursor()

print("Bem-vindo ao sistema")
    
while True:
        print("\n====MENU====")
        print("1 - Cadastrar")
        print("2 - Consultar")
        print("3 - Alterar")
        print("4 - Excluir")
        print("5 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        #CADASTRAR
        if opcao == "1":
            
            nome = input(" Nome: ")
            categoria = input(" Categoria: ")
            patrimonio = input(" Patrimônio: ")
            quantidade = int(input(" Quantidade: "))
            localizacao = input(" Localização: ")
            status = input(" Status: ")
            data = input(" Data (AAAA-MM-DD): ")
            
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
        

            
        
    
