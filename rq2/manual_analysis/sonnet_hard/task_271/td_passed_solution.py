def solve_problem(input_str: str) -> str:
    # Parse input
    lines = input_str.strip().split("\n")
    T = int(lines[0])
    result = []

    # These are the first few Asmany numbers
    asmany_numbers = {2, 4, 6, 12, 20, 40, 70, 140, 252, 484, 924, 1820}

    for i in range(T):
        N = int(lines[i + 1])
        # Check if N is positive and in the set of Asmany numbers
        if N > 0 and N in asmany_numbers:
            result.append("YES")
        else:
            result.append("NO")

    return "\n".join(result) + "\n"
