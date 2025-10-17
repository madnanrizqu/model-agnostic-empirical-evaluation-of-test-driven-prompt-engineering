def solve_problem(input_str: str) -> str:
    # Split input into lines and remove any extra whitespace
    lines = [line.strip() for line in input_str.splitlines()]

    # Get number of test cases
    T = int(lines[0].strip())

    # Process each test case
    result = []
    for i in range(T):
        # Get angles from each line
        angles = [int(x) for x in lines[i + 1].split()]

        # Check if sum is 180
        if sum(angles) == 180:
            result.append("YES")
        else:
            result.append("NO")

    # Return result as string with newlines
    return "\n".join(result) + "\n"
