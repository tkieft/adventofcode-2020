def run(program):
    pc = 0
    accumulator = 0
    instructionsVisited = set()

    while pc not in instructionsVisited:
        if pc >= len(program):
            return accumulator, "done"

        instructionsVisited.add(pc)
        opcode, val = program[pc]
        if opcode == "acc":
            accumulator += val
            pc += 1
        elif opcode == "jmp":
            pc += val
        elif opcode == "nop":
            pc += 1
        else:
            raise RuntimeError(f"Unrecognized instruction {opcode}")

    return accumulator, "loop"


def part2(program):
    for i in range(len(program)):
        if program[i][0] == "acc":
            continue
        newprogram = program.copy()

        if program[i][0] == "jmp":
            newprogram[i] = ("nop", program[i][1])
        elif program[i][0] == "nop":
            newprogram[i] = ("jmp", program[i][1])
        else:
            raise RuntimeError(f"Unrecognized instruction {program[i][0]}")

        accumulator, status = run(newprogram)
        if status == "done":
            return accumulator


def parseInput(filename):
    program = []
    with open(filename) as f:
        for line in f:
            line = line.split()
            program.append((line[0], int(line[1])))

    return program


if __name__ == "__main__":
    program = parseInput("input.txt")
    print(run(program)[0])
    print(part2(program))
