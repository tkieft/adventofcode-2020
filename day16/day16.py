import itertools
import re
from functools import reduce
from io import TextIOWrapper
from operator import mul


def parse_rules(f: TextIOWrapper):
    rules: dict[str, list[range]] = {}
    pattern = re.compile(r"^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$")
    while (match := re.match(pattern, f.readline())) != None:
        rules[match.group(1)] = [
            range(int(match.group(2)), int(match.group(3)) + 1),
            range(int(match.group(4)), int(match.group(5)) + 1),
        ]
    return rules


def parse_ticket(line: str):
    return [int(s) for s in line.split(",")]


def parse_input():
    with open("input.txt", "r") as f:
        rules = parse_rules(f)
        f.readline()
        my_ticket = parse_ticket(f.readline().strip())
        f.readline()
        f.readline()
        other_tickets = [parse_ticket(line) for line in f]

    return rules, my_ticket, other_tickets


def part1(
    rules: dict[str, list[range]], my_ticket: list[int], other_tickets: list[list[int]]
):
    all_ranges = list(itertools.chain(*rules.values()))
    invalid_value_sum = 0
    valid_tickets: list[list[int]] = []
    for ticket in other_tickets:
        for val in ticket:
            if not any(val in range for range in all_ranges):
                invalid_value_sum += val
                break
        else:
            valid_tickets.append(ticket)

    print(invalid_value_sum)
    return valid_tickets


def part2(
    rules: dict[str, list[range]], my_ticket: list[int], other_tickets: list[list[int]]
):
    field_possibilities: list[set[str]] = []
    for i in range(len(rules)):
        possibilities = set(rules.keys())
        for ticket in other_tickets:
            for field in possibilities.copy():
                if not any(ticket[i] in r for r in rules[field]):
                    possibilities.discard(field)
        field_possibilities.append(possibilities)

    field_order: dict[str, int] = {}
    for i in range(len(rules)):
        found_keys = [
            (i, s.pop()) for i, s in enumerate(field_possibilities) if len(s) == 1
        ]
        assert len(found_keys) == 1
        field_order[found_keys[0][1]] = found_keys[0][0]
        for s in field_possibilities:
            if found_keys[0][1] in s:
                s.remove(found_keys[0][1])

    departure_fields = [v for k, v in field_order.items() if k.startswith("departure")]
    print(reduce(mul, [my_ticket[field] for field in departure_fields]))


def main():
    rules, my_ticket, other_tickets = parse_input()
    valid_tickets = part1(rules, my_ticket, other_tickets)
    part2(rules, my_ticket, valid_tickets)


if __name__ == "__main__":
    main()
