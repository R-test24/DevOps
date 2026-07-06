import mysql.connector
from mysql.connector import Error
 
# Conexão com o banco de dados
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="teste"
    )
    mycursor = db.cursor(buffered=True)
    print("Conectado ao banco de dados MySQL!")
except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")
    exit()
 
listaTeste = []
 
class Estoque:
    def __init__(self, nomeItem, tipoItem, modeloItem, tamanhoItem, marcaItem, quantidadeItem, fornecedorItem, precoCompra, precoVenda):
        self.nomeItem = nomeItem
        self.tipoItem = tipoItem
        self.modeloItem = modeloItem
        self.tamanhoItem = tamanhoItem
        self.marcaItem = marcaItem
        self.quantidadeItem = quantidadeItem
        self.fornecedorItem = fornecedorItem
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda
 
    @staticmethod
    def cadastrarItem():
        nomeItem = input("Digite o nome do item a ser cadastrado: ")
       
        print("Escolha o tipo do item: ")
        print("1- Camiseta")
        print("2- Calça")
        print("3- Calção")
        print("4- Regata")
       
        while True:
            try:  
                escolha = int(input("Digite o número correspondente ao tipo do item: "))
                if 1 <= escolha <= 4:
                    break
                else:
                    print("Valor inválido. Por favor, insira um número entre 1 e 4.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número entre 1 e 4.")
       
        tipos = {1: "Camiseta", 2: "Calça", 3: "Calção", 4: "Regata"}
        tipoItem = tipos[escolha]
       
        # Modelo apenas para Camiseta e Regata
        if tipoItem in ["Camiseta", "Regata"]:
            print("Escolha o modelo do item: ")
            print("1- Manga Curta")
            print("2- Manga Longa")
            while True:
                try:  
                    escolha = int(input("Digite o número correspondente ao modelo do item: "))
                    if 1 <= escolha <= 2:
                        break
                    else:
                        print("Valor inválido. Por favor, insira um número entre 1 e 2.")
                except ValueError:
                    print("Valor inválido. Por favor, insira um número entre 1 e 2.")
           
            modelos = {1: "Manga Curta", 2: "Manga Longa"}
            modeloItem = modelos[escolha]
        else:
            modeloItem = "N/A"
       
        # Tamanho
        while True:
            tamanhoItem = input("Digite o tamanho do item (P, M, G, GG): ").upper()
            if tamanhoItem in ["P", "M", "G", "GG"]:
                break
            else:
                print("Valor inválido. Por favor, insira um dos seguintes tamanhos: P, M, G, GG.")
       
        marcaItem = input("Digite a marca do item: ")
       
        # Quantidade
        while True:
            try:
                quantidadeItem = int(input("Digite a quantidade do item: "))
                if quantidadeItem >= 0:
                    break
                else:
                    print("Valor inválido. A quantidade não pode ser negativa.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro.")
       
        fornecedorItem = input("Digite o fornecedor do item: ")
       
        # Preço de compra
        while True:
            try:
                precoCompra = float(input("Digite o preço de compra do item: "))
                if precoCompra >= 0:
                    break
                else:
                    print("Valor inválido. O preço de compra não pode ser negativo.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número.")
       
        # Preço de venda
        while True:
            try:
                precoVenda = float(input("Digite o preço de venda do item: "))
                if precoVenda >= 0 and precoVenda >= precoCompra:
                    break
                else:
                    print("Valor inválido. O preço de venda não pode ser negativo e deve ser maior ou igual ao preço de compra  .")
            except ValueError:
                print("Valor inválido. Por favor, insira um número.")
       
        # Inserir no banco de dados (id será gerado automaticamente)
        try:
            sql = """INSERT INTO itens (nome, tipo, modelo, tamanho, marca, quantidade,
                     fornecedor, preco_compra, preco_venda)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (nomeItem, tipoItem, modeloItem, tamanhoItem, marcaItem,
                      quantidadeItem, fornecedorItem, precoCompra, precoVenda)
           
            mycursor.execute(sql, valores)
            db.commit()
           
            print(f"\nItem '{nomeItem}' cadastrado com sucesso! ID gerado: {mycursor.lastrowid}\n")
        except Error as e:
            print(f"Erro ao cadastrar item no banco de dados: {e}")
            db.rollback()
 
    @staticmethod
    def consultarItem():
        nome_consulta = input("Digite o nome do item a ser consultado: ")
       
        try:
            sql = "SELECT * FROM itens WHERE nome LIKE %s"
            mycursor.execute(sql, (f"%{nome_consulta}%",))
            resultados = mycursor.fetchall()
           
            if resultados:
                print(f"\n{'='*50}")
                print(f"Encontrado(s) {len(resultados)} item(ns):")
                for item in resultados:
                    print(f"\n--- Item ID: {item[0]} (Auto increment) ---")
                    print(f"Nome: {item[1]}")
                    print(f"Tipo: {item[2]}")
                    print(f"Modelo: {item[3]}")
                    print(f"Tamanho: {item[4]}")
                    print(f"Marca: {item[5]}")
                    print(f"Quantidade: {item[6]}")
                    print(f"Fornecedor: {item[7]}")
                    print(f"Preço de Compra: R$ {item[8]:.2f}")
                    print(f"Preço de Venda: R$ {item[9]:.2f}")
                print(f"{'='*50}\n")
            else:
                print(f"Item '{nome_consulta}' não encontrado.\n")
        except Error as e:
            print(f"Erro ao consultar item: {e}")
 
# Programa principal
print("=== Sistema de Estoque ===\n")
 
# Verificar se a tabela existe
try:
    mycursor.execute("SELECT 1 FROM itens LIMIT 1")
    mycursor.fetchone()
except Error:
    print("A tabela 'itens' não existe no banco de dados 'estoque'.")
    print("Por favor, crie a tabela antes de continuar.")
    print("\nExemplo de criação da tabela:")
    print("""
    CREATE TABLE itens (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        tipo VARCHAR(50) NOT NULL,
        modelo VARCHAR(50),
        tamanho VARCHAR(5),
        marca VARCHAR(100),
        quantidade INT NOT NULL,
        fornecedor VARCHAR(255),
        preco_compra DECIMAL(10,2) NOT NULL,
        preco_venda DECIMAL(10,2) NOT NULL,
    );
    """)
    exit()
 
# Carregar itens existentes do banco para a listaTeste
try:
    mycursor.execute("SELECT * FROM itens")
    itens_db = mycursor.fetchall()
    for item in itens_db:
        # item[0] é o ID (auto increment), mas não será armazenado na classe
        item_obj = Estoque(item[1], item[2], item[3], item[4], item[5],
                          item[6], item[7], item[8], item[9])
        listaTeste.append({
            "ID": item[0],  # ID do banco
            "Nome": item_obj.nomeItem,
            "Tipo": item_obj.tipoItem,
            "Modelo": item_obj.modeloItem,
            "Tamanho": item_obj.tamanhoItem,
            "Marca": item_obj.marcaItem,
            "Quantidade": item_obj.quantidadeItem,
            "Fornecedor": item_obj.fornecedorItem,
            "Preço de Compra": item_obj.precoCompra,
            "Preço de Venda": item_obj.precoVenda
        })
    print(f"{len(listaTeste)} itens carregados do banco de dados.\n")
except Error as e:
    print(f"Erro ao carregar itens: {e}")
 
on = True
while on:
    print("Escolha uma opção: ")
    print("1- Cadastrar item")
    print("2- Consultar item")
    print("3- Sair")
   
    escolha = input("Digite o número correspondente à opção desejada: ")
   
    match escolha:
        case "1":
            Estoque.cadastrarItem()
        case "2":
            Estoque.consultarItem()
        case "3":
            on = False
            print("Encerrando o programa...")
            db.close()
        case _:
            print("Opção inválida. Por favor, digite 1, 2 ou 3.\n")