def solve_problem(input_str: str) -> str:
    # Split the input into lines
    lines = input_str.strip().split("\n")

    # First line is the number of test cases
    T = int(lines[0])

    # Dictionary to map class IDs to ship classes
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

    # Process each test case
    results = []
    for i in range(1, T + 1):
        char = lines[i].strip()
        if char in ship_classes:
            results.append(ship_classes[char])

    # Join results with newline and return
    return "\n".join(results)
