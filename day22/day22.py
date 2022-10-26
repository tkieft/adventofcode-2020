def parse_input(filename: str):
    p1: list[int] = []
    p2: list[int] = []
    with open(filename) as f:
        f.readline()
        while line := f.readline().strip():
            p1.append(int(line))
        f.readline()
        while line := f.readline().strip():
            p2.append(int(line))
    return p1, p2


def calculate_score(deck: list[int]):
    return sum([(i + 1) * v for i, v in enumerate(reversed(deck))])


def part1(p1: list[int], p2: list[int]):
    while p1 and p2:
        c1, c2 = p1.pop(0), p2.pop(0)
        if c1 > c2:
            p1.extend([c1, c2])
        else:
            p2.extend([c2, c1])
    winner = p2 if p2 else p1
    print(calculate_score(winner))


def play_recursive(p1: list[int], p2: list[int]):
    rounds: set[tuple[tuple[int], tuple[int]]] = set()

    round_count = 1
    while True:
        key = (tuple(p1), tuple(p2))
        if key in rounds:
            return 1, p1, p2
        rounds.add(key)

        c1, c2 = p1.pop(0), p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            winner, _, _ = play_recursive(p1[:c1], p2[:c2])
        elif c1 > c2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            p1.extend([c1, c2])
        else:
            p2.extend([c2, c1])

        if not p1:
            return 2, p1, p2
        elif not p2:
            return 1, p1, p2

        round_count += 1


def part2(p1: list[int], p2: list[int]):
    _, p1, p2 = play_recursive(p1, p2)
    winning_deck = p1 if p1 else p2
    print(calculate_score(winning_deck))


def main():
    p1, p2 = parse_input("input.txt")
    part1(p1.copy(), p2.copy())
    part2(p1.copy(), p2.copy())


if __name__ == "__main__":
    main()
