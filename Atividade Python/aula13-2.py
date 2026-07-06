cliente = {
    'nome': 'Ana Silva',
    'email': 'ana@email.com',
    'cidade': 'Florianópolis',
    'idade': 28
    
}

print(cliente['nome'])
print(cliente['email'])

# .get() - acessa sem gerar erro
print(cliente.get('rg'))
print(cliente.get('rg','N/A'))

#PERCORRER com .items()
for chave, valor in cliente.items():
    print(f'{chave}: {valor}')
    