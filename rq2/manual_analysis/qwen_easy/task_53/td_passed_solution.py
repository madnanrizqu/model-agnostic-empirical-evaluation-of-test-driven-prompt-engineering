import re


def solve_problem(input_str: str) -> str:

    # Define the mapping of class IDs to ship classes
    class_map = {"B": "BattleShip", "C": "Cruiser", "D": "Destroyer", "F": "Frigate"}

    # Split the input string into lines
    lines = input_str.strip().split("\n")

    # The first line is the number of test cases
    T = int(lines[0])

    # Process each test case
    result = []
    for i in range(1, T + 1):
        class_id = lines[i].strip().upper()
        if class_id in class_map:
            result.append(class_map[class_id])

    # Join the results with newline characters
    return "\n".join(result) + "\n"
