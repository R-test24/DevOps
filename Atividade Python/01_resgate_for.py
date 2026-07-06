# ============================================================
# AULA 12 — Resgate: for + range()
# Jovem Programador 2026 | SENAC SC
# ============================================================
#
# Revisão rápida do for antes de entrar em funções.
# O for percorre uma lista ou usa range() para repetir.
# ============================================================

print('Exemplo 1 ✅ com função for e range!')

print("=== Resgate 1: for no InfoStart — listar clientes ===")
print()

clientes = ["Ana Silva", "Bruno Costa", "Carlos Lima", "Rodrigo Costa"]

print("Clientes cadastrados:")
for i in range(len(clientes)):    # range(len()) = índice de cada item
    print(f"  {i + 1}. {clientes[i]}")

# i + 1 porque queremos mostrar 1, 2, 3 (não 0, 1, 2)

# ============================================================
# EXPERIMENTE:
# 1. Adicione mais clientes e veja a numeração automática.
# ============================================================

print(" Exemplo 2 ✅ com função range!")

# range(1, 6) cria a sequência
# list() transforma em lista para poder visualizar

print(list(range(1, 6)))

print ('Exemplo 3 ✅ com função range!')

print(list(range(5)))        # 0 até 4
print(list(range(0, 10, 2))) # de 2 em 2