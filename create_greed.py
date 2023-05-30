def knapsack_01(capacity, mineral):
    weights = list()
    values = list()

    for key,value in mineral.items():
        if key == 'peso':
            weights.append(value)
        elif key == 'valor':
            values.append(value)
            
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    
    selected_items = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i)
            w -= weights[i - 1]
        i -= 1
    
    return dp[n][capacity], selected_items[::-1]