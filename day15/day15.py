STARTING_NUMBERS = [9, 6, 0, 10, 18, 2, 1]


def solve(n):
    numbers = {n: [i] for i, n in enumerate(STARTING_NUMBERS)}
    current = STARTING_NUMBERS[-1]
    for i in range(len(STARTING_NUMBERS), n):
        if len(numbers[current]) == 1:
            current = 0
        else:
            current = numbers[current][-1] - numbers[current][-2]

        lasts = numbers.get(current, ())
        lasts = (lasts[-1], i) if len(lasts) > 0 else (i,)
        numbers[current] = lasts

    return current


if __name__ == "__main__":
    print(solve(2020))
    print(solve(30000000))
