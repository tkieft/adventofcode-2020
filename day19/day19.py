import itertools
import re
from io import TextIOWrapper
from typing import cast


def parse_rules(f: TextIOWrapper):
    rules: dict[int, list[list[int]] | str] = {}
    while (line := f.readline().strip()) != "":
        rule_id, rule = line.split(": ")
        rule_id = int(rule_id)
        if rule.startswith('"'):
            rules[rule_id] = rule[1]
        else:
            rules[rule_id] = [
                [int(x) for x in rule_part.strip().split(" ")]
                for rule_part in rule.split("|")
            ]
    return rules


def test_rules(rules: dict[int, list[list[int]] | str], start_rule: int = 0):
    valid_messages = set()
    patterns = cast(list[list[int]], rules[start_rule])
    while patterns:
        new_patterns = []
        for pattern in patterns:
            expansions = [[]]
            for c in pattern:
                if isinstance(c, str):
                    expansions = [e + [c] for e in expansions]
                    continue

                rule = rules[c]
                if isinstance(rule, str):
                    expansions = [e + [rule] for e in expansions]
                else:
                    new_expansions = []
                    for rule_part in rule:
                        new_expansions.extend([e + rule_part for e in expansions])
                    expansions = new_expansions
            new_patterns.extend(expansions)
        patterns = []
        for p in new_patterns:
            if all(isinstance(x, str) for x in p):
                valid_messages.add("".join(p))
            else:
                patterns.append(p)
    return valid_messages


def main():
    with open("input.txt") as f:
        rules = parse_rules(f)
        test_messages = [line.strip() for line in f]

    print("PART 1")
    valid_messages = test_rules(rules)
    print(len([p for p in test_messages if p in valid_messages]))

    print("PART 2")
    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31

    # Each pattern is 8 chars
    valid_42 = test_rules(rules, 42)
    valid_31 = test_rules(rules, 31)

    valid_count = 0
    for message in test_messages:
        count_42 = 0
        count_31 = 0
        while message and message[0:8] in valid_42:
            count_42 += 1
            message = message[8:]
        while message and message[0:8] in valid_31:
            count_31 += 1
            message = message[8:]
        if count_42 >= 2 and count_31 >= 1 and count_31 <= count_42 - 1 and not message:
            valid_count += 1

    print(valid_count)


if __name__ == "__main__":
    main()
