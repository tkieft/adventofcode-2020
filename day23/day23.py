from __future__ import annotations

from dataclasses import dataclass

TEST = "389125467"
INPUT = "712643589"


@dataclass
class Cups:
    head: Cup
    map: dict[int, Cup]


@dataclass
class Cup:
    label: int
    next: Cup | None = None

    def __repr__(self):
        return f"({self.label})"


def play(cups: Cups, moves: int):
    current = cups.head

    for _ in range(moves):
        next1 = current.next
        assert next1
        next2 = next1.next
        assert next2
        next3 = next2.next
        assert next3

        removed_values = [next1.label, next2.label, next3.label]

        current.next = next3.next
        dest = current.label - 1
        while dest <= 0 or dest in removed_values:
            dest = dest - 1
            if dest <= 0:
                dest = len(cups.map)

        dest_cup = cups.map[dest]
        next3.next = dest_cup.next
        dest_cup.next = next1

        assert current.next
        current = current.next


def parse(input: str, total: int | None = None) -> Cups:
    cup_map: dict[int, Cup] = {}
    head = None
    current = None
    for i in map(int, input):
        cup = Cup(i)
        cup_map[i] = cup
        if current:
            current.next = cup
            current = cup
        else:
            head = current = cup

    if total is not None:
        assert current is not None
        for i in range(len(input) + 1, total + 1):
            cup = Cup(i)
            cup_map[i] = cup
            current.next = cup
            current = cup

    assert current is not None
    assert head is not None
    current.next = head
    return Cups(head, cup_map)


def part1(input: str):
    cups = parse(input)
    play(cups, 100)
    cup1 = cups.map[1]
    current = cup1.next
    while current is not None and current != cup1:
        print(current.label, end="")
        current = current.next
    print()


def part2(input: str):
    cups = parse(input, 1_000_000)
    play(cups, 10_000_000)

    cup1 = cups.map[1]
    next1 = cup1.next
    assert next1
    next2 = next1.next
    assert next2
    print(next1.label * next2.label)


def main():
    part1(INPUT)
    part2(INPUT)


if __name__ == "__main__":
    main()
