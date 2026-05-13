import collections
import functools
import math
import time


PHRASE = "thereisasyetinsufficientdataforameaningfulanswer"
MAX_LENGTH = 15
COUNTER = collections.Counter(PHRASE)
LETTERS = tuple(sorted(COUNTER))
LETTER_INDEX = {letter: index for index, letter in enumerate(LETTERS)}
INITIAL_COUNTS = tuple(COUNTER[letter] for letter in LETTERS)


@functools.lru_cache(None)
def _suffix_count(counts, max_length):
    counts_by_length = [0] * (max_length + 1)
    counts_by_length[0] = 1
    for count in counts:
        next_counts = [0] * (max_length + 1)
        for length, value in enumerate(counts_by_length):
            if value:
                for used in range(min(count, max_length - length) + 1):
                    next_counts[length + used] += value * math.comb(length + used, used)
        counts_by_length = next_counts
    return sum(counts_by_length)


def position(word):
    counts = list(INITIAL_COUNTS)
    rank = 0
    for pos, letter in enumerate(word):
        remaining = MAX_LENGTH - pos - 1
        letter_index = LETTER_INDEX[letter]
        for smaller in range(letter_index):
            if counts[smaller]:
                counts[smaller] -= 1
                rank += _suffix_count(tuple(counts), remaining)
                counts[smaller] += 1

        counts[letter_index] -= 1
        if pos < len(word) - 1:
            rank += 1
    return rank + 1


def wordAtPosition(position_value):
    counts = list(INITIAL_COUNTS)
    output = []
    while len(output) < MAX_LENGTH:
        remaining = MAX_LENGTH - len(output) - 1
        for index, letter in enumerate(LETTERS):
            if not counts[index]:
                continue
            counts[index] -= 1
            block = _suffix_count(tuple(counts), remaining)
            if position_value > block:
                position_value -= block
                counts[index] += 1
                continue

            output.append(letter)
            if position_value == 1:
                return "".join(output)
            position_value -= 1
            break
    return "".join(output)


def lastQuestion():
    target = (
        position("legionary")
        + position("calorimeters")
        - position("annihilate")
        + position("orchestrated")
        - position("fluttering")
    )
    return wordAtPosition(target)


def runTests():
    assert wordAtPosition(10) == "aaaaaacdee"
    assert position("aaaaaacdee") == 10
    assert wordAtPosition(115_246_685_191_495_243) == "euler"
    assert position("euler") == 115_246_685_191_495_243


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = lastQuestion()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
