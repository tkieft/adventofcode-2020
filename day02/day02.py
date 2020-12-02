import re

PATTERN = re.compile(r"(\d+)-(\d+) (\w): (\w+)")

def valid(low, high, char, password):
    count = password.count(char)
    return count >= low and count <= high

def valid2(pos1, pos2, char, password):
    return (password[pos1 - 1] == char) ^ (password[pos2 - 1] == char)

def parseLine(line):
    m = PATTERN.match(line)
    return (int(m[1]), int(m[2]), m[3], m[4])

if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [parseLine(line) for line in f]

    print(sum(valid(*line) for line in lines))
    print(sum(valid2(*line) for line in lines))
