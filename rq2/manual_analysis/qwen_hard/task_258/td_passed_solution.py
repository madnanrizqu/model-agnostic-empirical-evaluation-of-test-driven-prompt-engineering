from typing import List


def solve_problem(input_str: str) -> str:
    lines = input_str.strip().split("\n")
    N = int(lines[0])
    friends = [list(map(int, line)) for line in lines[1:]]

    suggestions = 0

    for u in range(N):
        for v in range(N):
            if u == v or friends[u][v] == 1:
                continue
            for w in range(N):
                if w == u or w == v:
                    continue
                if friends[u][w] == 1 and friends[v][w] == 1:
                    suggestions += 1
                    break

    return str(suggestions) + "\n"
