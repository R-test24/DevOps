import random

ELEMENTOS_DO_SORTEIO = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def sortear(elementos, fazerGanhar):
  elementosSorteados = []
  
  elementosSorteados.append(random.choice(elementos))  # ex.: [0]
  
  if fazerGanhar:
    elementosSorteados.append(elementosSorteados[0]) # ex.: [0, 0]
    elementosSorteados.append(elementosSorteados[0]) # ex.: [0, 0, 0]
  
  else:
    elementosSorteados.append(random.choice(elementos)) # ex.: [0, 0]
    elementosSorteados.append(random.choice(elementos)) # ex.: [0, 0, 0]
    
    while (elementosSorteados[0] == elementosSorteados[1] == elementosSorteados[2]):
      indice = random.randint(0, 2) # ex.: 1
      elementosSorteados[indice] = random.choice(elementos) # ex.: [0, 1, 0]
  
  return elementosSorteados
  
contadorDeUsuarios = 1

for i in range(15):
  
  fazerGanhar = False

  if contadorDeUsuarios == 1 or contadorDeUsuarios == 2 or (contadorDeUsuarios % 4) == 0:
    fazerGanhar = True
    
  elementosSorteados = sortear(ELEMENTOS_DO_SORTEIO, fazerGanhar)
  
  print(contadorDeUsuarios, elementosSorteados, fazerGanhar)
  contadorDeUsuarios += 1
