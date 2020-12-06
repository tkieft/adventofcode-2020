def anyAnsweredYes(group):
    questions = set()
    for person in group:
        questions |= set(person)
    return len(questions)

def allAnsweredYes(group):
    questions = set(group[0])
    for person in group[1:]:
        questions &= set(person)
    return len(questions)

def parseInput(filename):
    groups = []
    group = []
    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                groups.append(group)
                group = []
                continue

            group.append(line.strip())

    if group != []:
        groups.append(group)

    return groups

if __name__ == "__main__":
    groups = parseInput("input.txt")
    print(sum(anyAnsweredYes(group) for group in groups))
    print(sum(allAnsweredYes(group) for group in groups))
