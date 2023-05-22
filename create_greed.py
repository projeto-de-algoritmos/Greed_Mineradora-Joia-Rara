def knapsack_problem(caminhhao, capacidade):
    n = len(caminhhao)
    tabela = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, capacidade + 1):
            if caminhhao[i - 1][1] <= j:
                tabela[i][j] = max(caminhhao[i - 1][0] + tabela[i - 1][j - caminhhao[i - 1][1]], tabela[i - 1][j])
            else:
                tabela[i][j] = tabela[i - 1][j]

    valor_maximo = tabela[n][capacidade]
    peso_total = capacidade
    minerios_selecionados = []

    for i in range(n, 0, -1):
        if valor_maximo <= 0:
            break
        if valor_maximo == tabela[i - 1][peso_total]:
            continue
        else:
            minerios_selecionados.append(caminhhao[i - 1])
            valor_maximo -= caminhhao[i - 1][0]
            peso_total -= caminhhao[i - 1][1]

    return minerios_selecionados

# Exemplo de uso, cada minerio é uma tupla (lista) contendo (valor, peso)
caminhhao = [
    (10, 2),  # Minerio 1: valor = 10, peso = 2
    (5, 3),   # Minerio 2: valor = 5, peso = 3
    (15, 5),  # Minerio 3: valor = 15, peso = 5
    (7, 7)    # Minerio 4: valor = 7, peso = 7
]

capacidade_do_caminhao = 500

minerios_selecionados = knapsack_problem(capacidade_do_caminhao)

print("Minerios selecionados:")
for minerio in minerios_selecionados:
    print(f"Valor: {minerio[0]}, Peso: {minerio[1]}")
