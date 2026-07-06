print("=== Exemplo1: Repetir até digitar um numero positivo ===")
print()

numero = int(input("Digite um numero positivo: "))
while numero <= 0:
    print("Número inválido! Precisa ser mairo que zero.")
    numero = int(input("Tente nvamente: "))

print (f"Ótimo! Você digitou: {numero}")
print()
