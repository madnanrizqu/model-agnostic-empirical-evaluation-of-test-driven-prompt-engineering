def solve_problem(input_str: str) -> str:
    # Parse input
    lines = input_str.strip().split("\n")
    N = int(lines[0])

    # Create adjacency matrix
    friends = [[0] * N for _ in range(N)]
    for i in range(N):
        row = lines[i + 1]
        for j in range(N):
            if row[j] == "1":
                friends[i][j] = 1
                friends[j][i] = 1

    suggestions = set()

    # For each potential common friend w
    for w in range(N):
        # Get all friends of w
        w_friends = []
        for i in range(N):
            if friends[w][i] and i != w:
                w_friends.append(i)

        # For each pair of w's friends
        for i in range(len(w_friends)):
            u = w_friends[i]
            for j in range(i + 1, len(w_friends)):
                v = w_friends[j]
                # If they're not already friends, add suggestion
                if not friends[u][v]:
                    # Add both ordered pairs to ensure uniqueness
                    suggestions.add((min(u, v), max(u, v)))

    return str(len(suggestions)) + "\n"
