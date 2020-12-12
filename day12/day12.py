from enum import Enum
import math

DIRS = {"E": 0, "N": 90, "W": 180, "S": 270}
DEGS = {v: k for k, v in DIRS.items()}

def turn(currentDirection, degrees):
    return DEGS[(DIRS[currentDirection] + degrees) % 360]

def part1(directions):
    currentDirection = "E"
    x = 0
    y = 0

    for direction in directions:
        action = direction[0]

        if action == "L":
            currentDirection = turn(currentDirection, direction[1])
        elif action == "R":
            currentDirection = turn(currentDirection, -direction[1])
        elif action == "F":
            action = currentDirection

        if action == "E":
            x += direction[1]
        elif action == "N":
            y += direction[1]
        if action == "W":
            x -= direction[1]
        elif action == "S":
            y -= direction[1]

    return abs(x) + abs(y)


def part2(directions):
    x = 0
    y = 0

    wx = 10
    wy = 1

    for direction in directions:
        action = direction[0]

        if action == "L" or action == "R":
            angle = math.atan2(wy, wx) + (1 if action == "L" else -1) * math.radians(direction[1])
            hypot = math.hypot(wx, wy)
            wx = round(math.cos(angle) * hypot)
            wy = round(math.sin(angle) * hypot)
        elif action == "F":
            x += wx * direction[1]
            y += wy * direction[1]
        elif action == "E":
            wx += direction[1]
        elif action == "N":
            wy += direction[1]
        if action == "W":
            wx -= direction[1]
        elif action == "S":
            wy -= direction[1]

        print(f"{direction} {x} {y} {wx} {wy}")

    return abs(x) + abs(y)


def parseInput(filename):
    with open(filename) as f:
        return [(line[0], int(line[1:])) for line in f]


if __name__ == "__main__":
    directions = parseInput("input.txt")
    print(part1(directions))
    print(part2(directions))
