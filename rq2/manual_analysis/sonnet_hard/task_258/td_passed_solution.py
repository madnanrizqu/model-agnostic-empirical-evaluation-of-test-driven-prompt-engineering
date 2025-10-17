def solve_problem(input_str: str) -> str:
    # Parse input
    lines = input_str.strip().split("\n")
    N = int(lines[0])

    # Create adjacency matrix
    friends = [[1 if c == "1" else 0 for c in lines[i + 1]] for i in range(N)]

    suggestions = 0

    # For each pair of users
    for u in range(N):
        for v in range(N):
            # Skip if they are already friends or same user
            if u == v or friends[u][v]:
                continue

            # Check if they have a common friend
            for w in range(N):
                # w must be different from both u and v
                if w != u and w != v and friends[u][w] and friends[v][w]:
                    suggestions += 1
                    break

    return f"{suggestions}\n"
