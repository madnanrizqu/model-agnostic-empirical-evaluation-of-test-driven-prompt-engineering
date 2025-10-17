from math import gcd


def solve_problem(input_str: str) -> str:
    lines = input_str.strip().split("\n")
    n = int(lines[0])
    results = []

    for i in range(1, n + 1):
        a, b = lines[i].split()
        a = int(a)
        b = int(b)
        # Calculate GCD
        results.append(str(gcd(a, b)))

    return "\n".join(results) + "\n"
