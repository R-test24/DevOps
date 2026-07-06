# Capturando os dados do cliente
nome =input("Digite o nome do cliente:")
cpf =input("Digite o CPF:")
idade =input ("Digite sua idade:")

if idade >= 18:
     print("Idade válido")
else:
     print("Idade inválido! Precisa ser >18.")
          
email =input("Digite e-mail:")

if "@" in email:
     print("E-mail válido!")  
else:
     print("E-mail inválido! Precisa ter '@'.")


# Exibindo o resumo do cadastro

print()
()
print("--DADOS CADASTRADOS--")
print(f"Nome: {nome}")
print(f"CPF:  {cpf}")
print(f"Idade:  {idade}")
print(f"E-mail:  {email}")

      
print()

print("Cadastro registro com sucesso!")


