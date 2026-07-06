while True:
    nome = input('Nome do Produto:')
    if len(nome)>0: 
        break
print('Produto não pode estar em banco.')
  
# Campo cpf:repete até ter 11 digitos numéricos

while True:
    Codigo = input ('codigo (6 numeros):')
    if len(Codigo)== 6 and Codigo.isdigit():
     # cpf.isdigit()- True se todos forem números 
         break
    print(f'codigo invalido! Digitou {len(Codigo)} caracteres.')
print()