from typing import List


def solve_problem(input_str: str) -> str:
    # Split the input string into lines
    lines = input_str.strip().split("\n")
    # The first line is the number of test cases
    T = int(lines[0])
    # The following lines are the class IDs
    class_ids = lines[1:]

    # Dictionary to map class IDs to class descriptions
    class_descriptions = {
        "B": "BattleShip",
        "b": "BattleShip",
        "C": "Cruiser",
        "c": "Cruiser",
        "D": "Destroyer",
        "d": "Destroyer",
        "F": "Frigate",
        "f": "Frigate",
    }

    # List to store the results
    results = []

    # Iterate over each class ID and get the corresponding description
    for class_id in class_ids:
        description = class_descriptions.get(class_id, "Unknown Class")
        results.append(description)

    # Join the results with newline characters and return
    return "\n".join(results)
