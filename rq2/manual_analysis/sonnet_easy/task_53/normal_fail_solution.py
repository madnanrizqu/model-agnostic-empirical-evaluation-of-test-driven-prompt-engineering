def solve_problem(input_str: str) -> str:
    # Dictionary mapping ship class IDs to their descriptions
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

    # Get number of test cases
    T = int(lines[0])

    # Process each test case
    result = []
    for i in range(T):
        ship_id = lines[i + 1]
        result.append(ship_classes[ship_id])

    # Return result as string with newlines
    return "\n".join(result)
