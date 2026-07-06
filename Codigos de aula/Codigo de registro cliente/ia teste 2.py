import pymysql

usuario = input("Usuário: ")
senha = input("Senha: ")

try:
    conexao = pymysql.connect(
        host="localhost",
        user=usuario,
        password=senha,
        database="escola"
    )

    cursor = conexao.cursor()

    while True:

        print("\n===== MENU =====")
        print("1 - Cadastrar")
        print("2 - Consultar")
        print("3 - Alterar")
        print("4 - Excluir")
        print("5 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":

            nome = input("Nome: ")
            categoria = input("Categoria: ")
            patrimonio = input("Patrimônio: ")
            quantidade = int(input("Quantidade: "))
            localizacao = input("Localização: ")
            status = input("Status: ")
            data = input("Data (AAAA-MM-DD): ")

            sql = """
            INSERT INTO equipamentos
            (nome,categoria,patrimonio,quantidade,
             localizacao,status,data_cadastro)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            valores = (
                nome, categoria, patrimonio,
                quantidade, localizacao,
                status, data
            )

            cursor.execute(sql, valores)
            conexao.commit()

            print("Equipamento cadastrado!")

        elif opcao == "2":

            cursor.execute("SELECT * FROM equipamentos")

            for equipamento in cursor.fetchall():
                print(equipamento)

        elif opcao == "3":

            id_equipamento = input("ID: ")
            novo_status = input("Novo status: ")

            sql = """
            UPDATE equipamentos
            SET status=%s
            WHERE id_equipamento=%s
            """

            cursor.execute(
                sql,
                (novo_status, id_equipamento)
            )

            conexao.commit()

            print("Atualizado!")

        elif opcao == "4":

            id_equipamento = input("ID: ")

            sql = """
            DELETE FROM equipamentos
            WHERE id_equipamento=%s
            """

            cursor.execute(sql, (id_equipamento,))
            conexao.commit()

            print("Excluído!")

        elif opcao == "5":
            break

        else:
            print("Opção inválida!")

    conexao.close()

except Exception as erro:
    print("Erro:", erro)