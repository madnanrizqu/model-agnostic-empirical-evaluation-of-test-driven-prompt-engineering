def solve_problem(input_str: str) -> str:
    # Dictionary to map ship IDs to their class names
    ship_classes = {
        "B": "BattleShip",
        "b": "BattleShip",
        "C": "Cruiser",
        "c": "Cruiser",
        "D": "Destroyer",
        "d": "Destroyer",
        "F": "Frigate",
        "f": "Frigate",
    }

    # Split input into lines
    lines = input_str.strip().split("\n")

    # First line contains number of test cases
    T = int(lines[0])

    # Process each test case
    result = []
    for i in range(T):
        ship_id = lines[i + 1].strip()
        result.append(ship_classes[ship_id])

    # Return result as string with newlines
    return "\n".join(result) + "\n"
