def solve_problem(input_str: str) -> str:
    # Parse the input
    data = input_str.split()
    T = int(data[0])  # Number of test cases
    index = 1
    results = []

    for _ in range(T):
        N = int(data[index])  # Size of array A
        index += 1
        A = list(map(int, data[index : index + N]))
        index += N

        # Calculate the total sum of XOR-sums F(L, R)
        total_sum = 0
        freq = [0] * 32  # To store the frequency of set bits at each position

        for i in range(N):
            # Update the total sum with the contribution of A[i]
            for bit in range(32):
                if A[i] & (1 << bit):
                    total_sum += (1 << bit) * (i - freq[bit])
                    freq[bit] += 1
                else:
                    total_sum += (1 << bit) * freq[bit]

        results.append(total_sum)

    # Return the results as a single string
    return "\n".join(map(str, results))
