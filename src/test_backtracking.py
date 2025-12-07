from backtracking import solve_backtracking


adj = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
}
k = 3

result = solve_backtracking(adj, k)
print(result)
