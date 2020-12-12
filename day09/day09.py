def part1(nums):
    for i in range(25, len(nums)):
        foundSum = False
        for j in range(i - 25, i - 1):
            for k in range(i - 24, i):
                if nums[i] == nums[j] + nums[k]:
                    foundSum = True
                    break
            if foundSum:
                break

        if not foundSum:
            return nums[i]

def part2(nums, goal):
    for i in range(len(nums)):
        sum = 0
        for j in range(i, len(nums)):
            sum += nums[j]
            if sum == goal:
                return min(nums[i:j]) + max(nums[i:j])
            elif sum > goal:
                break


def parseInput(filename):
    with open(filename) as f:
        nums = [int(line) for line in f]

    return nums

if __name__ == "__main__":
    nums = parseInput("input.txt")
    goal = part1(nums)
    print(goal)
    print(part2(nums, goal))
