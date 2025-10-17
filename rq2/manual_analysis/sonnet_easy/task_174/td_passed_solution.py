def solve_problem(input_str: str) -> str:
    # Split input into lines
    lines = input_str.strip().split("\n")

    # Get number of test cases
    T = int(lines[0])

    result = []
    # Process each test case
    for i in range(T):
        # Get angles from each line
        angles = list(map(int, lines[i + 1].split()))

        # Check if sum is 180 and all angles are greater than 0
        if sum(angles) == 180 and all(angle > 0 for angle in angles):
            result.append("YES")
        else:
            result.append("NO")

    # Return result as string with newlines
    return "\n".join(result) + "\n"
