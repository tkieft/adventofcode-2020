import re

PATTERN = re.compile(r"([FB]+)([RL]+)")

def seatID(row, col):
    row = int(row.replace("F", "0").replace("B", "1"), base=2)
    col = int(col.replace("L", "0").replace("R", "1"), base=2)
    return row * 8 + col

def parseInput(filename):
    passes = []
    with open(filename) as f:
        for line in f:
            match = PATTERN.match(line)
            passes.append((match.group(1), match.group(2)))

    return passes


if __name__ == "__main__":
    passes = parseInput("input.txt")
    seatIDs = [seatID(*p) for p in passes]
    seatIDs.sort()

    print(seatIDs[-1])

    for i, s in enumerate(seatIDs):
        if seatIDs[i + 1] != s + 1:
            print(s + 1)
            break
