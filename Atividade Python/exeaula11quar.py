print( "Exemplo 1: Validar e-mail xom while true")
print()

while True:
    email= input("Digite seu e-mail: ")

    if"@" in email:
        print(f"🟢 E-mail aceito: {email}")
        break
    else:
     print(" ❌ E-mail inválido! Precisa ter @. Tente novamente. ")
    print()
    
