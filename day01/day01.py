def part1(numlist, numset):
    for num in numlist:
        if (2020 - num) in numlist:
            return num * (2020 - num)

def part2(numlist, numset):
    for i, num in enumerate(numlist):
        for j, num2 in enumerate(numlist[i:]):
            if (2020 - num - num2) in numset:
                return num * num2 * (2020 - num - num2)


if __name__ == "__main__":
    with open("input.txt") as f:
        numlist = [int(line) for line in f]
    numset = set(numlist)

    print(part1(numlist, numset))
    print(part2(numlist, numset))
