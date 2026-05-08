import collections
import math
import time
from pathlib import Path


def readWords():
    path = Path(__file__).resolve().parents[1] / "Files" / "p098_words.txt"
    return [word.strip('"') for word in path.read_text().strip().split(",")]


def pattern(value):
    indexes = {}
    result = []

    for char in value:
        if char not in indexes:
            indexes[char] = len(indexes)
        result.append(indexes[char])

    return tuple(result)


def groupedAnagrams(words):
    groups = collections.defaultdict(list)
    for word in words:
        groups["".join(sorted(word))].append(word)
    return [group for group in groups.values() if len(group) > 1]


def squareStringsByLengthAndPattern(lengths):
    squares = collections.defaultdict(list)

    for length in lengths:
        lower = math.isqrt(10 ** (length - 1) - 1) + 1
        upper = math.isqrt(10 ** length - 1)
        for root in range(lower, upper + 1):
            square = str(root * root)
            squares[(length, pattern(square))].append(square)

    return squares


def mappingFor(word, square):
    letters_to_digits = {}
    digits_to_letters = {}

    for letter, digit in zip(word, square):
        if letter in letters_to_digits and letters_to_digits[letter] != digit:
            return None
        if digit in digits_to_letters and digits_to_letters[digit] != letter:
            return None
        letters_to_digits[letter] = digit
        digits_to_letters[digit] = letter

    return letters_to_digits


def applyMapping(word, mapping):
    if mapping[word[0]] == "0":
        return None
    return "".join(mapping[letter] for letter in word)


def largestAnagramicSquare(words):
    groups = groupedAnagrams(words)
    lengths = {len(word) for group in groups for word in group}
    square_lookup = squareStringsByLengthAndPattern(lengths)
    square_sets = {
        length: set(square for squares in square_lookup.values() for square in squares if len(square) == length)
        for length in lengths
    }
    best = 0

    for group in groups:
        for first_index, first_word in enumerate(group):
            for second_word in group[first_index + 1 :]:
                key = (len(first_word), pattern(first_word))
                for first_square in square_lookup[key]:
                    mapping = mappingFor(first_word, first_square)
                    if mapping is None:
                        continue

                    second_square = applyMapping(second_word, mapping)
                    if second_square in square_sets[len(second_word)]:
                        best = max(best, int(first_square), int(second_square))

    return best


def runTests():
    assert largestAnagramicSquare(["CARE", "RACE"]) == 9216


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = largestAnagramicSquare(readWords())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
