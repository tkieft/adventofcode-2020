from __future__ import annotations

import re
from collections import defaultdict

Coord = tuple[int, int]
Tiles = dict[Coord, bool]

WHITE = False
BLACK = True


DIR_REGEX = re.compile("e|w|se|sw|ne|nw")
DIRS_TO_COORDS = {
    "e": (2, 0),
    "w": (-2, 0),
    "se": (1, 1),
    "sw": (-1, 1),
    "ne": (1, -1),
    "nw": (-1, -1),
}


def add_coords(coord1: Coord, coord2: Coord) -> Coord:
    return tuple(x + y for x, y in zip(coord1, coord2))


def neighbor_count(tiles: Tiles, coord: Coord):
    counts = {WHITE: 0, BLACK: 0}
    for c in DIRS_TO_COORDS.values():
        new_coord = add_coords(coord, c)
        counts[tiles[new_coord]] += 1
    return counts


def count_black(tiles: Tiles):
    return sum(tiles.values())


def parse_input(filename: str):
    return [re.findall(DIR_REGEX, line) for line in open(filename) if line]


def part1(lines: list[list[str]]):
    tiles: Tiles = defaultdict(lambda: WHITE)
    for line in lines:
        coord = (0, 0)
        for dir in line:
            coord = add_coords(coord, DIRS_TO_COORDS[dir])
        tiles[coord] = not tiles[coord]
    return tiles


def part2(tiles: Tiles):
    for i in range(100):
        new_tiles: Tiles = defaultdict(lambda: WHITE)
        x_coords, y_coords = zip(*tiles)

        # Include buffer (2 for x, 1 for y)
        for x in range(min(x_coords) - 2, max(x_coords) + 3):
            for y in range(min(y_coords) - 1, max(y_coords) + 2):
                coord = (x, y)
                counts = neighbor_count(tiles, coord)
                if tiles[coord] == WHITE and counts[BLACK] == 2:
                    new_tiles[coord] = BLACK
                elif tiles[coord] == BLACK and (
                    counts[BLACK] == 0 or counts[BLACK] > 2
                ):
                    pass
                elif tiles[coord] == BLACK:
                    # Only keep track of black tiles to reduce memory
                    new_tiles[coord] = tiles[coord]

        tiles = new_tiles

    return tiles


def main():
    lines = parse_input("input.txt")
    tiles = part1(lines)
    print(count_black(tiles))
    tiles = part2(tiles)
    print(count_black(tiles))


if __name__ == "__main__":
    main()
