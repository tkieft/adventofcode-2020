from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Protocol

DIGIT = re.compile(r"\d")


class Node(Protocol):
    pass


def calculate(o1: int, oper: str, o2: int):
    if oper == "+":
        return o1 + o2
    elif oper == "*":
        return o1 * o2
    else:
        raise ValueError(f"Invalid operator {oper}")


@dataclass
class OperandNode(Node):
    val: int

    def evaluate(self):
        return self.val

    def __str__(self) -> str:
        return f"{self.val}"


@dataclass
class OperatorNode(Node):
    operator: str


@dataclass
class CompoundNode(Node):
    operator: OperatorNode
    left: OperandNode | CompoundNode
    right: OperandNode | CompoundNode

    def evaluate(self):
        return calculate(
            self.left.evaluate(), self.operator.operator, self.right.evaluate()
        )

    def __str__(self) -> str:
        left = (
            f"{self.left}" if isinstance(self.left, OperandNode) else f"({self.left})"
        )
        right = (
            f"{self.right}"
            if isinstance(self.right, OperandNode)
            else f"({self.right})"
        )
        return f"{left} {self.operator.operator} {right}"


def create_tree(line: str, index: int = 0) -> tuple[OperandNode | CompoundNode, int]:
    i = index
    root = None
    operator = ""
    while i < len(line):
        c = line[i]
        if c == " ":
            i += 1
            continue
        if c == ")":
            assert root is not None
            return root, i

        if c == "(":
            operand, i = create_tree(line, i + 1)
        elif re.match(DIGIT, c):
            operand = OperandNode(int(c))
        else:
            operator = c
            i += 1
            continue

        if root is None:
            root = operand
            i += 1
            continue
        else:
            root = CompoundNode(OperatorNode(operator), root, operand)
            i += 1

    assert root is not None
    return root, i


def create_tree_2(line: str, index: int = 0) -> tuple[OperandNode | CompoundNode, int]:
    stack: list[Node] = []
    i = index
    while i < len(line):
        c = line[i]
        if c == " ":
            i += 1
            continue
        if c == ")":
            break

        if c == "*" or c == "+":
            stack.append(OperatorNode(c))
        else:
            if c == "(":
                operand, i = create_tree_2(line, i + 1)
            else:
                operand = OperandNode(int(c))

            if len(stack) == 0:
                stack.append(operand)
            else:
                node = stack[-1]
                assert isinstance(node, OperatorNode)
                if node.operator == "+":
                    stack.pop()
                    left = stack.pop()
                    assert isinstance(left, OperandNode | CompoundNode)
                    stack.append(CompoundNode(node, left, operand))
                else:
                    stack.append(operand)

        i += 1

    while len(stack) > 1:
        right = stack.pop()
        operator = stack.pop()
        left = stack.pop()
        assert isinstance(left, OperandNode | CompoundNode)
        assert isinstance(right, OperandNode | CompoundNode)
        assert isinstance(operator, OperatorNode)
        stack.append(CompoundNode(operator, left, right))

    result = stack.pop()
    assert isinstance(result, OperandNode | CompoundNode)
    return result, i


def sumlines(fn: Callable[[str], int]):
    sum = 0
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sum += fn(line)
    print(sum)


def part1():
    sumlines(lambda l: create_tree(l)[0].evaluate())


def part2():
    sumlines(lambda l: create_tree_2(l)[0].evaluate())


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
