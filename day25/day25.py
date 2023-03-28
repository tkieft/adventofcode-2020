from __future__ import annotations

SUBJECT_NUMBER = 7

CARD_PUBLIC_KEY = 17607508
DOOR_PUBLIC_KEY = 15065270


def transform(value: int, subject_number: int):
    return value * subject_number % 20201227


def transform_loop(subject_number: int, loop_size: int):
    value = 1
    for _ in range(loop_size):
        value = transform(value, subject_number)
    return value


def find_loop_size(public_key: int, start_value: int):
    value = start_value
    i = 0
    while True:
        i += 1
        value = transform(value, SUBJECT_NUMBER)
        if value == public_key:
            return i


def main():
    card_loop_size = find_loop_size(CARD_PUBLIC_KEY, 1)
    door_loop_size = find_loop_size(DOOR_PUBLIC_KEY, 1)
    print(transform_loop(CARD_PUBLIC_KEY, door_loop_size))
    print(transform_loop(DOOR_PUBLIC_KEY, card_loop_size))


if __name__ == "__main__":
    main()
