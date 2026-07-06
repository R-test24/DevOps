import pymysql

try:
    conexao = pymysql.connect(
        host="localhost",
        user="admin",
        password="1234",
        database="escola"
    )

    cursor = conexao.cursor()

    print("Conectado com sucesso!")

    while True:

        print("\n===== MENU =====")
        print("1 - Cadastrar")
        print("2 - Consultar")
        print("3 - Alterar")
        print("4 - Excluir")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        # CADASTRAR
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
            (nome, categoria, patrimonio, quantidade,
            localizacao, status, data_cadastro)
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

            cursor.execute(sql, valores)
            conexao.commit()

            print("Equipamento cadastrado com sucesso!")

        # CONSULTAR
        elif opcao == "2":

            sql = "SELECT * FROM equipamentos"

            cursor.execute(sql)

            equipamentos = cursor.fetchall()

            print("\n=== EQUIPAMENTOS ===\n")

            for equipamento in equipamentos:
                print(equipamento)

        # ALTERAR
        elif opcao == "3":

            id_equipamento = input(
                "Digite o ID do equipamento: "
            )

            novo_status = input(
                "Novo status: "
            )

            sql = """
            UPDATE equipamentos
            SET status = %s
            WHERE id_equipamento = %s
            """

            cursor.execute(
                sql,
                (novo_status, id_equipamento)
            )

            conexao.commit()

            print("Equipamento alterado!")

        # EXCLUIR
        elif opcao == "4":

            id_equipamento = input(
                "Digite o ID do equipamento: "
            )

            sql = """
            DELETE FROM equipamentos
            WHERE id_equipamento = %s
            """

            cursor.execute(sql, (id_equipamento,))

            conexao.commit()

            print("Equipamento excluído!")

        # SAIR
        elif opcao == "5":

            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida!")

    conexao.close()

except Exception as erro:
    print("Erro ao conectar:", erro)