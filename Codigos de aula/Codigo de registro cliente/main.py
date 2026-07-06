print( "=== CADASTRO DE CLIENTE ===" )

nome = input("Digite seu nome: ")
cpf = input("Digite seu CPF: ")
email = input("Digite seu email: ")

print("\n--- Dados Cadastrados ---")
print("Nome: ", nome)
print("CPF: ", cpf)
print("Email: ", email)

if "@" not in email:
 print("Email invalido! Precisa ter @")
else:
 print("Cadastro realizado com sucesso!")
 