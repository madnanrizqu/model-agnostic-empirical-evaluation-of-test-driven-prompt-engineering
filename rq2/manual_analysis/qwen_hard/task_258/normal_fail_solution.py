from typing import List


def solve_problem(input_str: str) -> str:
    lines = input_str.strip().split("\n")
    N = int(lines[0])
    friends = [list(map(int, line)) for line in lines[1:]]

    suggestions = 0

    for u in range(N):
        for v in range(u + 1, N):
            if friends[u][v] == 0:
                common_friends = sum(
                    friends[u][w] and friends[v][w]
                    for w in range(N)
                    if w != u and w != v
                )
                suggestions += common_friends

    return str(suggestions)
