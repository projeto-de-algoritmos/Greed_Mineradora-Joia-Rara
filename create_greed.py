def knapsack_problem(caixa_ferramentas, capacidade):
    n = len(caixa_ferramentas)
    tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacidade + 1):
            if caixa_ferramentas[i - 1][1] <= j:
                tabela[i][j] = max(caixa_ferramentas[i - 1][0] + tabela[i - 1][j - caixa_ferramentas[i - 1][1]], tabela[i - 1][j])
            else:
                tabela[i][j] = tabela[i - 1][j]

    valor_maximo = tabela[n][capacidade]
    peso_total = capacidade
    ferramentas_selecionadas = []

    for i in range(n, 0, -1):
        if valor_maximo <= 0:
            break
        if valor_maximo == tabela[i - 1][peso_total]:
            continue
        else:
            ferramentas_selecionadas.append(caixa_ferramentas[i - 1])
            valor_maximo -= caixa_ferramentas[i - 1][0]
            peso_total -= caixa_ferramentas[i - 1][1]

    return ferramentas_selecionadas

# Exemplo de uso
# Cada ferramenta é uma tupla contendo (valor, peso)
caixa_ferramentas = [
    (10, 2),  # Ferramenta 1: valor = 10, peso = 2
    (5, 3),   # Ferramenta 2: valor = 5, peso = 3
    (15, 5),  # Ferramenta 3: valor = 15, peso = 5
    (7, 7)    # Ferramenta 4: valor = 7, peso = 7
]

capacidade_caixa = 10

ferramentas_selecionadas = knapsack_problem(caixa_ferramentas, capacidade_caixa)

print("Ferramentas selecionadas:")
for ferramenta in ferramentas_selecionadas:
    print(f"Valor: {ferramenta[0]}, Peso: {ferramenta[1]}")
