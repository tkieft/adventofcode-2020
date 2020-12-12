def printArea(area):
    for row in area:
        print(''.join(row))
    print()

def copyArea(area):
    return [row.copy() for row in area]

def neighbors(area, y, x):
    result = 0

    for i in range(max(0, y - 1), min(len(area), y + 2)):
        for j in range(max(0, x - 1), min(len(area[y]), x + 2)):
            if i == y and j == x: continue
            if area[i][j] == '#':
                result += 1

    return result


def neighbors2(area, y, x):
    result = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue

            yy = y + i
            xx = x + j
            while True:
                if yy < 0 or yy >= len(area): break
                if xx < 0 or xx >= len(area[yy]): break
                if area[yy][xx] == '#':
                    result += 1
                    break
                if area[yy][xx] == 'L':
                    break
                yy += i
                xx += j

    return result


def part1(area):
    while True:
        previous = copyArea(area)

        for y, row in enumerate(previous):
            for x, seat in enumerate(row):
                if seat == '.': continue

                n = neighbors(previous, y, x)
                if seat == '#' and n >= 4:
                    area[y][x] = 'L'
                elif seat == 'L' and n == 0:
                    area[y][x] = '#'

        if previous == area:
            return sum(row.count('#') for row in area)

def part2(area):
    while True:
        previous = copyArea(area)

        for y, row in enumerate(previous):
            for x, seat in enumerate(row):
                if seat == '.': continue

                n = neighbors2(previous, y, x)
                if seat == '#' and n >= 5:
                    area[y][x] = 'L'
                elif seat == 'L' and n == 0:
                    area[y][x] = '#'

        if previous == area:
            return sum(row.count('#') for row in area)

def parseInput(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f]


if __name__ == "__main__":
    area = parseInput("input.txt")
    print(part1(copyArea(area)))
    print(part2(area))
