def solve_problem(input_str: str) -> str:
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Parse the input
    lines = input_str.strip().split("\n")
    n = int(lines[0])  # Number of test cases
    results = []

    for i in range(1, n + 1):
        a, b = lines[i].split()
        a = int(a)
        # Reduce b modulo a for large numbers
        b_mod_a = (
            int(b) % a
            if len(b) <= 18
            else sum(
                (int(digit) * (10**idx)) % a for idx, digit in enumerate(reversed(b))
            )
            % a
        )
        results.append(gcd(a, b_mod_a))

    # Return results as a string with each result on a new line
    return "\n".join(map(str, results))
