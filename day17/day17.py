import itertools

BOARD_TYPE = dict[tuple[int, ...], bool]


def parse_input(filename: str, dimens: int):
    board: BOARD_TYPE = {}
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip()):
                coord = (i, j) + (0,) * (dimens - 2)
                board[coord] = c == "#"
    return board


def get_active_neighbor_count(board: BOARD_TYPE, coord: tuple[int, ...], dimens: int):
    return sum(
        [
            board.get(c, False)
            for c in itertools.product(
                *[range(coord[i] - 1, coord[i] + 2) for i in range(dimens)]
            )
            if c != coord
        ]
    )


def run_simulation(board: BOARD_TYPE, dimens: int):
    mins = tuple(min(x[i] for x in board) for i in range(dimens))
    maxes = tuple(max(x[0] for x in board) for i in range(dimens))

    new_board: BOARD_TYPE = {}

    for c in itertools.product(
        *[range(mins[i] - 1, maxes[i] + 2) for i in range(dimens)]
    ):
        active_neighbor_count = get_active_neighbor_count(board, c, dimens)
        if board.get(c, False):
            if active_neighbor_count in range(2, 4):
                new_board[c] = True
        else:
            if active_neighbor_count == 3:
                new_board[c] = True

    return new_board


def part1(board: BOARD_TYPE):
    for _ in range(6):
        board = run_simulation(board, 3)
    print(len(board))


def part2(board: BOARD_TYPE):
    for _ in range(6):
        board = run_simulation(board, 4)
    print(len(board))


def main():
    part1(parse_input("input.txt", 3))
    part2(parse_input("input.txt", 4))


if __name__ == "__main__":
    main()
