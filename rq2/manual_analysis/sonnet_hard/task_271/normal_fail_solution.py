def solve_problem(input_str: str) -> str:
    # Parse input
    lines = input_str.strip().split("\n")
    T = int(lines[0])
    result = []

    # Pre-calculated first few Asmany numbers
    # These are the counts of valid strings for each length
    # For length 2: 2 strings (01,10)
    # For length 4: 4 strings (0011,1100,0101,1010)
    asmany_numbers = {2, 4, 8, 16, 32, 64, 128, 256}

    for i in range(T):
        N = int(lines[i + 1])
        if N in asmany_numbers:
            result.append("YES")
        else:
            result.append("NO")

    # Return result with newline at the end
    return "\n".join(result) + "\n"
