from pathlib import Path


NAMES_FILE = Path("Files/p022_names.txt")


def loadNames(path=NAMES_FILE):
    text = path.read_text().strip()
    return sorted(name.strip('"') for name in text.split(","))


def alphabeticalValue(name):
    return sum(ord(char) - ord("A") + 1 for char in name)


def nameScore(name, position):
    return alphabeticalValue(name) * position


def totalNameScores(names):
    return sum(nameScore(name, index) for index, name in enumerate(names, start=1))


def runTests():
    assert alphabeticalValue("COLIN") == 53
    assert nameScore("COLIN", 938) == 49714


def solve():
    return totalNameScores(loadNames())


if __name__ == "__main__":
    runTests()
    print(solve())
