from math import isqrt


def solve_problem(input_str: str) -> str:
    def max_phi_over_i(N):
        if N == 2:
            return 2
        if N == 3:
            return 3
        # Start with the assumption that the maximum is at 3
        max_i = 3
        max_value = 2 / 3
        # Check for numbers of the form 2^k * 3^m
        for k in range(1, 65):  # 2^64 is a very large number, more than 10^18
            for m in range(1, 65):
                i = (2**k) * (3**m)
                if i > N:
                    break
                phi_i = i * (1 - 1 / 2) * (1 - 1 / 3)
                value = phi_i / i
                if value > max_value:
                    max_value = value
                    max_i = i
        return max_i

    lines = input_str.strip().split("\n")
    T = int(lines[0])
    results = []
    for i in range(1, T + 1):
        N = int(lines[i])
        results.append(str(max_phi_over_i(N)))
    return "\n".join(results)
