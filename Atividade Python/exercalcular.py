def calcular_desconto(preco, percentual):
    desconto = preco *(percentual / 100)
    preco_final = preco - desconto
    return preco_final #devolve o resultado

preco_com_desconto = calcular_desconto(100, 50)
print(f'Preço com 20% de desconto: R$ {preco_com_desconto}')
print()

