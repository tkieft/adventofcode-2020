import itertools
import re

LINE_REGEX = re.compile(r"(^.+) \(contains (.+)\)$")


def parse_input(filename: str):
    foods: list[tuple[set[str], set[str]]] = []
    with open(filename) as f:
        for line in f:
            if line := line.strip():
                match = LINE_REGEX.match(line)
                assert match
                foods.append(
                    (set(match.group(1).split()), set(match.group(2).split(", ")))
                )
    return foods


def part1(foods: list[tuple[set[str], set[str]]]):
    allergen_dict: dict[str, set[str]] = {}

    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in allergen_dict:
                allergen_dict[allergen] = set(ingredients)
            else:
                allergen_dict[allergen].intersection_update(ingredients)

    processed = set()
    while len(allergen_dict) != len(processed):
        allergen, ingredients = next(
            (k, v)
            for k, v in allergen_dict.items()
            if not k in processed and len(v) == 1
        )
        processed.add(allergen)
        for k, v in allergen_dict.items():
            if k != allergen:
                v.difference_update(ingredients)

    final_allergens = {k: v.pop() for k, v in allergen_dict.items()}

    all_ingredients = set(itertools.chain(*[food[0] for food in foods]))
    safe_ingredients = all_ingredients.difference(
        list(itertools.chain(final_allergens.values()))
    )

    safe_ingredients_count = sum(
        len(ingredients.intersection(safe_ingredients)) for ingredients, _ in foods
    )
    print(safe_ingredients_count)

    return final_allergens


def part2(allergen_dict: dict[str, str]):
    allergens = sorted([(k, v) for k, v in allergen_dict.items()], key=lambda t: t[0])
    print(",".join(a[1] for a in allergens))


def main():
    foods = parse_input("input.txt")
    allergen_dict = part1(foods)
    part2(allergen_dict)


if __name__ == "__main__":
    main()
