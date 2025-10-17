def solve_problem(input_str: str) -> str:
    input_lines = input_str.splitlines()
    T = int(input_lines[0])  # Number of test cases
    results = []
    idx = 1

    for _ in range(T):
        N = int(input_lines[idx])  # Size of array A
        A = list(map(int, input_lines[idx + 1].split()))
        idx += 2

        # Calculate the total sum of XOR-sums F(L, R) over all L and R
        total_sum = 0
        freq = [0] * (N + 1)
        xor_prefix = 0

        for i in range(N):
            xor_prefix ^= A[i]
            total_sum += xor_prefix * (i + 1) - sum(freq[: i + 1])
            freq[i + 1] = xor_prefix

        results.append(str(total_sum))

    return "\n".join(results)
