# Campo Nome: repete até não estar vazio

while True:
    nome = input('Nome do cliente:')
    if len(nome)>0: 
        break
print('Nome não pode estar em banco.')
  
# Campo cpf:repete até ter 11 digitos numéricos

while True:
    cpf = input ('cpf (11 numeros):')
    if len(cpf)== 11 and cpf.isdigit():
     # cpf.isdigit()- True se todos forem números 
         break
    print(f'cpf invalido! Digitou {len(cpf)} caracteres.')

while True:
    idade_texto = input('idade')
    if not idade_texto.isdigit():
        print('Digite apenas números.')
        continue
    idade = int(idade_texto)
    if idade >=18:
        break
