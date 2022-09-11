import re

MASK_REGEX = re.compile(r"^mask = (.+)$")
MEM_REGEX = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def part1(filename):
    mem = {}
    with open(filename) as f:
        for line in f:
            if match := MASK_REGEX.match(line):
                mask = match.group(1)
            elif match := MEM_REGEX.match(line):
                address = int(match.group(1))
                value = int(match.group(2))
                masked_value = (value | int(mask.replace("X", "0"), 2)) & int(
                    mask.replace("X", "1"), 2
                )
                mem[address] = masked_value
            else:
                raise ValueError("Invalid line format")

    return sum(mem.values())


def part2(filename):
    mem = {}
    with open(filename) as f:
        for line in f:
            if match := MASK_REGEX.match(line):
                mask = match.group(1)
                floaters = [i for i, x in enumerate(mask) if x == "X"]
            elif match := MEM_REGEX.match(line):
                address = list(
                    format(
                        int(match.group(1)) | int(mask.replace("X", "0"), 2), "b"
                    ).zfill(36)
                )
                value = int(match.group(2))

                for i in range(pow(2, len(floaters))):
                    for i, c in enumerate(format(i, "b").zfill(len(floaters))):
                        address[floaters[i]] = c

                    mem[int("".join(address), 2)] = value
            else:
                raise ValueError("Invalid line format")

    return sum(mem.values())


if __name__ == "__main__":
    print(part1("input.txt"))
    print(part2("input.txt"))
