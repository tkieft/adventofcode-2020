import re

PATTERN = re.compile(r"(\w+ \w+) bags contain (.+)\.")
PATTERN2 = re.compile(r"(\d+) (\w+ \w+) bag")

class Node:
    def __init__(self, name):
        self.name = name
        self.containers = []
        self.contained = []

    def addContainer(self, node):
        self.containers.append(node)

    def addContained(self, node, quantity):
        self.contained.append((node, quantity))


def findContainers(node):
    containers = set(node.containers)
    for c in node.containers:
        containers |= findContainers(c)
    return containers

def findContained(node):
    return sum(findContained(c) * quantity + quantity for c, quantity in node.contained)

def parseInput(filename):
    nodes = {}
    with open(filename) as f:
        for line in f:
            match = PATTERN.match(line)
            containerName = match.group(1)
            container = nodes.get(containerName)
            if not container:
                container = Node(containerName)
                nodes[containerName] = container

            for match2 in PATTERN2.finditer(match.group(2)):
                containedName = match2.group(2)
                containedQuantity = int(match2.group(1))
                contained = nodes.get(containedName)
                if not contained:
                    contained = Node(containedName)
                    nodes[containedName] = contained

                contained.addContainer(container)
                container.addContained(contained, containedQuantity)

    return nodes


if __name__ == "__main__":
    bags = parseInput("input.txt")
    print(len(findContainers(bags["shiny gold"])))
    print(findContained(bags["shiny gold"]))
