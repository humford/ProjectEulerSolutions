from math import isqrt
from pathlib import Path


WORDS_FILE = Path("Files/p042_words.txt")


def loadWords(path=WORDS_FILE):
    text = path.read_text().strip()
    return [word.strip('"') for word in text.split(",")]


def wordValue(word):
    return sum(ord(char) - ord("A") + 1 for char in word)


def isTriangleNumber(value):
    root = isqrt(8 * value + 1)
    return root * root == 8 * value + 1 and (root - 1) % 2 == 0


def triangleWordCount(words):
    return sum(1 for word in words if isTriangleNumber(wordValue(word)))


def runTests():
    assert wordValue("SKY") == 55
    assert isTriangleNumber(55)


def solve():
    return triangleWordCount(loadWords())


if __name__ == "__main__":
    runTests()
    print(solve())
