def exibir_cliente(nome, cidade):
    print(f'Cliente: {nome} ---Cidade: {cidade}')
#0 f é o q eu quero q traga pra mim. Ex nome.
exibir_cliente('Ana', 'Florianópolis')
exibir_cliente('Bruno', 'Blumenau')

#Parametros com  valor padrão
def exibir_status(nome, status='Ativo'):
    print(f'{nome}: {status}')

exibir_status('Ana')      # usa 'Ativo' automaticamente
exibir_status('Bruno','Inativo')  #sobreescreve o padrão
