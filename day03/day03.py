from collections import namedtuple
from functools import reduce
from operator import mul

Point = namedtuple("Point", "x y")
Point.__add__ = lambda point, other: Point(point.x + other.x, point.y + other.y)

SLOPES = [
    Point(3, 1),
    Point(1, 1),
    Point(5, 1),
    Point(7, 1),
    Point(1, 2),
]

def countTrees(map, slope):
    pos = Point(0, 0)
    trees = 0

    while pos.y < len(map):
        row = map[pos.y]
        if row[pos.x % len(row)] == '#':
            trees += 1
        pos = pos + slope

    return trees


if __name__ == "__main__":
    with open("input.txt") as f:
        map = [list(line.strip()) for line in f]

    print(countTrees(map, SLOPES[0]))
    print(reduce(mul, (countTrees(map, slope) for slope in SLOPES), 1))
