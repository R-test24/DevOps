listaTeste = []
 
class Estoque:
    def __init__(self, idItem, nomeItem, tipoItem, modeloItem, tamanhoItem, marcaItem, quantidadeItem, fornecedorItem, precoCompra, precoVenda):
        self.idItem = idItem
        self.nomeItem = nomeItem
        self.tipoItem = tipoItem
        self.modeloItem = modeloItem
        self.tamanhoItem = tamanhoItem
        self.marcaItem = marcaItem
        self.quantidadeItem = quantidadeItem
        self.fornecedorItem = fornecedorItem
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda
 
    def cadastrarItem(self):
        self.idItem = self.idItem + 1
        while True:
            self.nomeItem = input("Digite o nome do item a ser cadastrado: ")
            if self.nomeItem.strip():
                break
            print("Valor inválido. O nome do item não pode ser vazio.")
 
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
                print("Valor inválido. Por favor, insira um número entre 1 e 4.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número entre 1 e 4.")
        if escolha < 1 or escolha > 4:
            print("Valor inválido. Por favor, insira um número entre 1 e 4.")
            self.cadastrarItem()
        else:
            print("Tipo do item selecionado: ", end="")
        match escolha:
            case 1:
                self.tipoItem = "Camiseta"
            case 2:
                self.tipoItem = "Calça"
            case 3:
                self.tipoItem = "Calção"
            case 4:
                self.tipoItem = "Regata"
 
        if self.tipoItem == "Camiseta" or self.tipoItem == "Regata":
            print("Escolha o modelo do item: ")
            print("1- Manga Curta")
            print("2- Manga Longa")
            while True:
                try:  
                    escolha = int(input("Digite o número correspondente ao modelo do item: "))
                    if 1 <= escolha <= 2:
                        break
                    print("Valor inválido. Por favor, insira um número entre 1 e 2.")
                except ValueError:
                    print("Valor inválido. Por favor, insira um número entre 1 e 2.")
            if escolha < 1 or escolha > 2:
                print("Valor inválido. Por favor, insira um número entre 1 e 2.")
                self.cadastrarItem()
            else:
                print("Modelo do item selecionado: ", end="")
            match escolha:
                case 1:
                    self.modeloItem = "Manga Curta"
                case 2:
                    self.modeloItem = "Manga Longa"
        else:
            self.modeloItem = "N/A"
 
        print("Escolha o tamanho do item: ")
        escolha = input("Digite o número correspondente ao tamanho do item (P, M, G, GG): ").upper()
        if escolha not in ["P", "M", "G", "GG"]:
            print("Valor inválido. Por favor, insira um dos seguintes tamanhos: P, M, G, GG.")
            while True:
                escolha = input("Digite o Tamanho correspondente ao tamanho do item (P, M, G, GG): ").upper()
                if escolha in ["P", "M", "G", "GG"]:
                    break
                else:
                    print("Valor inválido. Por favor, insira um dos seguintes tamanhos: P, M, G, GG.")
        self.tamanhoItem = escolha
 
        while True:
            self.marcaItem = input("Digite a marca do item: ")
            if self.marcaItem.strip():
                break
            print("Valor inválido. A marca do item não pode ser vazio.")
 
        while True:
            try:
                self.quantidadeItem = int(input("Digite a quantidade do item: "))
                if self.quantidadeItem < 0:
                    print("Valor inválido. A quantidade não pode ser negativa.")
                else:
                    break
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro para a quantidade.")
       
        while True:
            try:
                self.fornecedorItem = input("Digite o fornecedor do item: ")
                if self.fornecedorItem.strip():
                    break
                print("Valor inválido. O fornecedor do item não pode ser vazio.")
            except ValueError:
                print("Valor inválido. Por favor, insira um nome para o fornecedor.")
 
        while True:
            try:
                self.precoCompra = float(input("Digite o preço de compra do item: "))
                if self.precoCompra >= 0:
                    break
                print("Valor inválido. Por favor, insira um número para o preço de compra.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número para o preço de compra.")
       
        while True:
            try:
                self.precoVenda = float(input("Digite o preço de venda do item: "))
                if self.precoVenda > 0 and self.precoVenda >= self.precoCompra:
                    break
                print("Valor inválido. Por favor, insira um número para o preço de venda.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número para o preço de venda.")
 
        listaTeste.append({"ID": self.idItem, "Nome": self.nomeItem, "Tipo": self.tipoItem, "Modelo": self.modeloItem, "Tamanho": self.tamanhoItem, "Marca": self.marcaItem, "Quantidade": self.quantidadeItem, "Fornecedor": self.fornecedorItem, "Preço de Compra": self.precoCompra, "Preço de Venda": self.precoVenda})
 
    def consultarItem(self):
        # Primeiro, mostrar lista de IDs e Nomes
        print("\n=== Itens disponíveis ===")
        for item in listaTeste:
            print(f"ID: {item['ID']} - Nome: {item['Nome']}")
        print("========================\n")
       
        consulta = input("Digite o ID ou nome do item a ser consultado: ")
       
        # Tentar converter para inteiro se for número
        try:
            consulta_id = int(consulta)
            consulta_eh_numero = True
        except ValueError:
            consulta_eh_numero = False
       
        encontrado = False
        for item in listaTeste:
            if consulta_eh_numero:
                if item["ID"] == consulta_id:  # Comparação com inteiro
                    encontrado = True
                    break
            else:
                if item["Nome"].lower() == consulta.lower():
                    encontrado = True
                    break
       
        if encontrado:
            print("\n=== Item encontrado ===")
            print(f"ID: {item['ID']}")
            print(f"Nome: {item['Nome']}")
            print(f"Tipo: {item['Tipo']}")
            print(f"Modelo: {item['Modelo']}")
            print(f"Tamanho: {item['Tamanho']}")
            print(f"Marca: {item['Marca']}")
            print(f"Quantidade: {item['Quantidade']}")
            print(f"Fornecedor: {item['Fornecedor']}")
            print(f"Preço de Compra: {item['Preço de Compra']}")
            print(f"Preço de Venda: {item['Preço de Venda']}")
            print("======================\n")
        else:
            print("Item não encontrado.\n")
 
c1 = Estoque(1,"Camiseta Opel", "Camiseta", "Manga Curta", "P", "Nike", 10, "Fornecedor A", 50.0, 100.0)
on = True
while on:
    print("Escolha uma opção: ")
    print("1- Cadastrar item")
    print("2- Consultar item")
    print("3- Sair")
    while True:
        try:
            escolha = input("Digite o número correspondente à opção desejada: ")
            if escolha in ["1", "2", "3"]:
                break
            else:
                print("Valor inválido. Por favor, insira um número entre 1 e 3.")
        except ValueError:
            print("Valor inválido. Por favor, insira um número entre 1 e 3.")
 
    match escolha:
        case "1":
            c1.cadastrarItem()
        case "2":
            c1.consultarItem()
        case "3":
            on = False
            print("Encerrando o programa...")
        case _:
            print("Opção inválida. Por favor, digite 1, 2 ou 3.")