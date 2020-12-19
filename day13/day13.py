import math
import re

matcher = re.compile(r"\d+")

def part1(timestamp, buses):
    leaveat, bus = min((math.ceil(timestamp / b) * b, b) for b in buses)
    return bus * (leaveat - timestamp)


def part2(buses):
    # Chinese Remainder Theorem
    M = math.prod(bus for timestamp, bus in buses)
    result = 0
    for timestamp, bus in buses:
        ni = int(M / bus)
        nii = pow(ni, -1, bus)
        ci = bus - timestamp

        result += ni * nii * ci

    return result % M

def parseInput(filename):
    with open(filename) as f:
        timestamp = int(f.readline())
        buses = [(i, int(bus)) for i, bus in enumerate(f.readline().split(",")) if matcher.match(bus)]
        return timestamp, buses


if __name__ == "__main__":
    timestamp, buses = parseInput("input.txt")
    print(part1(timestamp, [bus for (i, bus) in buses]))
    print(part2(buses))
