from datetime import date, datetime
print("=== Módulo datetima ==")
print()
#date.today() - data de hoje
hoje = date.today()
print(f"Hoje é: {hoje}")
print(f"Ano: `{hoje.year}")

print()

#datetime.now() - data e hora atual

def calcular_idade(ano, mes, dia):
    hoje = date.today()
    nascimento = date(ano, mes, dia)
    idade = hoje.year - nascimento.year
    
    # Ajuste: se ainda não fez aniversário
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1
    
    return idade
# Testando com datas diferentes
idade = calcular_idade(2003, 1, 15)
print(f"Nascido em 20/06/2008 🔜 {idade} anos")


