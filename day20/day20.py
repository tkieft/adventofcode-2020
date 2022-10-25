from __future__ import annotations

import operator
import re
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce

# fmt: off
SEA_MONSTER_TOP =    re.compile(r"(?=.{18}#.)") # lookahead so we can get overlapping matches
SEA_MONSTER_MIDDLE = re.compile(r"#.{4}##.{4}##.{4}###")
SEA_MONSTER_BOTTOM = re.compile(r".#..#..#..#..#..#...")
SEA_MONSTER_HASH_COUNT = 15
# fmt: on


class Edge(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


def _rotate(board: list[str]):
    return ["".join(l[i] for l in board[::-1]) for i in range(len(board))]


@dataclass
class Tile:
    id: int
    board: list[str]

    def __repr__(self) -> str:
        return f"Tile {self.id}:\n" + "\n".join(self.board) + "\n"

    @property
    def top_edge(self):
        return self.board[0]

    @property
    def bottom_edge(self):
        return self.board[-1]

    @property
    def left_edge(self):
        return "".join([l[0] for l in self.board])

    @property
    def right_edge(self):
        return "".join([l[-1] for l in self.board])

    def rotate(self):
        self.board = _rotate(self.board)

    def flip(self):
        self.board.reverse()

    def edge(self, e: Edge):
        return {
            Edge.TOP: self.top_edge,
            Edge.RIGHT: self.right_edge,
            Edge.BOTTOM: self.bottom_edge,
            Edge.LEFT: self.left_edge,
        }[e]

    def trim_border(self):
        return [s[1:-1] for s in self.board[1:-1]]


def parse_input(filename: str):
    tiles: list[Tile] = []
    with open(filename) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            match = re.match(r"^Tile (\d+):$", line)
            assert match
            tile_id = int(match.group(1))
            tiles.append(Tile(tile_id, [f.readline().strip() for _ in range(10)]))
            f.readline()  # consume empty line
    return tiles


# Could optimize this to not repeat work but fuck it
def line_em_up(tiles: list[Tile]):
    # Arbitrarily assign the first tile to be at (0, 0)
    # We don't need the coordinates to be normalized
    matches: dict[tuple[int, int], Tile] = {(0, 0): tiles.pop()}

    while tiles:
        new = tiles.pop(0)
        for (x, y), tile in matches.items():
            neighbors = {
                (Edge.TOP, Edge.BOTTOM): (x, y - 1),
                (Edge.RIGHT, Edge.LEFT): (x + 1, y),
                (Edge.BOTTOM, Edge.TOP): (x, y + 1),
                (Edge.LEFT, Edge.RIGHT): (x - 1, y),
            }
            match = None
            for (e1, e2), coord in neighbors.items():
                if matches.get(coord):
                    continue

                for i in range(8):
                    if tile.edge(e1) == new.edge(e2):
                        match = coord
                        break
                    if i == 3:
                        new.flip()
                    else:
                        new.rotate()

                if match:
                    break
            if match:
                matches[match] = new
                break
        else:
            # No match yet, place back in the pile
            tiles.append(new)

    return matches


def find_bounds(matches: dict[tuple[int, int], Tile]):
    xr = range(min(c[0] for c in matches), max(c[0] for c in matches) + 1)
    yr = range(min(c[1] for c in matches), max(c[1] for c in matches) + 1)
    # Error check, make sure there's a tile in every space
    for x in xr:
        for y in yr:
            assert matches.get((x, y))
    return xr, yr


def part_1(matches: dict[tuple[int, int], Tile], xr: range, yr: range):
    # Find the corners and multiply their ids together
    print(
        reduce(
            operator.mul,
            [
                tile.id
                for tile in [
                    matches[c]
                    for c in [
                        (xr.start, yr.start),
                        (xr.stop - 1, yr.start),
                        (xr.start, yr.stop - 1),
                        (xr.stop - 1, yr.stop - 1),
                    ]
                ]
            ],
        )
    )


def create_board(
    matches: dict[tuple[int, int], Tile], xr: range, yr: range, tile_size: int
):
    raw_board: list[list[str]] = [[] for _ in range(len(yr) * (tile_size - 2))]
    for i, y in enumerate(yr):
        for x in xr:
            tile = matches[(x, y)]
            for j, line in enumerate(tile.trim_border()):
                raw_board[i * (tile_size - 2) + j].append(line)
    return ["".join(lines) for lines in raw_board]


def part_2(matches: dict[tuple[int, int], Tile], xr: range, yr: range, tile_size: int):
    board = create_board(matches, xr, yr, tile_size)
    monsters_found = 0

    # Rotate the board until we find some matches
    for i in range(8):
        monsters_found = 0
        for j in range(len(board) - 2):
            for match in SEA_MONSTER_TOP.finditer(board[j]):
                if SEA_MONSTER_MIDDLE.match(
                    board[j + 1], match.start()
                ) and SEA_MONSTER_BOTTOM.match(board[j + 2], match.start()):
                    monsters_found += 1
        if monsters_found:
            print(f"{monsters_found} sea monsters found")
            break

        if i == 3:
            board.reverse()
        else:
            board = _rotate(board)

    hash_count = sum(sum([c == "#" for c in line]) for line in board)
    # naive, but it works because sea monsters can't overlap
    print(hash_count - monsters_found * SEA_MONSTER_HASH_COUNT)


def main():
    tiles = parse_input("input.txt")
    tile_size = len(tiles[0].bottom_edge)
    matches = line_em_up(tiles)
    xr, yr = find_bounds(matches)
    part_1(matches, xr, yr)
    part_2(matches, xr, yr, tile_size)


if __name__ == "__main__":
    main()
