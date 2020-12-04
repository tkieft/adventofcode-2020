import re

ALL = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
REQUIRED = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

YEAR = re.compile(r"^\d{4}$")
HEIGHT = re.compile(r"^(\d+)(cm|in)$")
HAIRCOLOR = re.compile(r"^#[0-9a-f]{6}$")
EYECOLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
PASSID = re.compile(r"^\d{9}$")

def parseInput(filename):
    passports = []
    passport = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "":
                passports.append(passport)
                passport = {}
                continue
            for field in line.split():
                name, value = field.split(":")
                passport[name] = value

    if len(passport) > 0:
        passports.append(passport)

    return passports

def fieldsPresent(passport):
    for field in REQUIRED:
        if not field in passport:
            return False

    return True

def validYear(year, low, high):
    match = YEAR.match(year)
    if not match:
        return False
    year = int(year)
    return year >= low and year <= high

def validHeight(height):
    match = HEIGHT.match(height)
    if not match:
        return False
    value, unit = int(match.group(1)), match.group(2)

    if unit == "cm" and value >= 150 and value <= 193:
        return True
    if unit == "in" and value >= 59 and value <= 76:
        return True

    return False

def valid(passport):
    if not fieldsPresent(passport):
        return False

    if not validYear(passport["byr"], 1920, 2002):
        return False

    if not validYear(passport["iyr"], 2010, 2020):
        return False

    if not validYear(passport["eyr"], 2020, 2030):
        return False

    if not validHeight(passport["hgt"]):
        return False

    if not HAIRCOLOR.match(passport["hcl"]):
        return False

    if passport["ecl"] not in EYECOLORS:
        return False

    if not PASSID.match(passport["pid"]):
        return False

    return True


if __name__ == "__main__":
    passports = parseInput("input.txt")

    print(sum(fieldsPresent(passport) for passport in passports))
    print(sum(valid(passport) for passport in passports))
