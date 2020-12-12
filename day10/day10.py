def part1(adapters):
    diff1 = 0
    diff3 = 0

    for i, adapter in enumerate(adapters[1:]):
        diff = adapter - adapters[i]
        if diff == 1:
            diff1 += 1
        elif diff == 3:
            diff3 += 1

    return diff1 * diff3


def part2(adapters):
    options = [0] * len(adapters)
    options[0] = 1

    for i, adapter in enumerate(adapters):
        for j in range(i - 3, i):
            if j < 0:
                continue

            print(adapter - adapters[j])
            if adapter - adapters[j] <= 3:
                options[i] += options[j]

    return options[-1]


def parseInput(filename):
    with open(filename) as f:
        adapters = [int(line) for line in f]

    adapters.insert(0, 0)
    adapters.sort()
    adapters.append(adapters[-1] + 3)

    return adapters


if __name__ == "__main__":
    adapters = parseInput("input.txt")
    print(part1(adapters))
    print(part2(adapters))
