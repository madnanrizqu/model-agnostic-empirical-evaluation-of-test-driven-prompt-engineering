from math import isqrt


def solve_problem(input_str: str) -> str:
    def max_phi_over_i(N):
        if N == 2:
            return 2
        result = 2
        max_value = 0.5
        for i in range(3, N + 1):
            phi = i
            n = i
            p = 2
            while p * p <= n:
                if n % p == 0:
                    while n % p == 0:
                        n //= p
                    phi -= phi // p
                p += 1
            if n > 1:
                phi -= phi // n
            value = phi / i
            if value > max_value:
                max_value = value
                result = i
        return result

    lines = input_str.strip().split("\n")
    T = int(lines[0])
    results = []
    for i in range(1, T + 1):
        N = int(lines[i])
        results.append(str(max_phi_over_i(N)))
    return "\n".join(results) + "\n"
