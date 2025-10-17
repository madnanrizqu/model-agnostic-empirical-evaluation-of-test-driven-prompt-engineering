def solve_problem(input_str: str) -> str:
    # Mapping of class IDs to ship classes
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

    # Split the input into lines
    lines = input_str.strip().split("\n")

    # First line is the number of test cases
    T = int(lines[0])

    # Process each test case
    results = []
    for i in range(1, T + 1):
        char = lines[i]
        results.append(ship_classes[char])

    # Join results with newline and return
    return "\n".join(results) + "\n"
