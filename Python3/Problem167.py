import collections
import heapq
import time


PERIODS = {
    5: 32,
    7: 26,
    9: 444,
    11: 1628,
    13: 5906,
    15: 80,
    17: 126960,
    19: 380882,
    21: 2097152,
}

FUNDAMENTAL_DIFFERENCES = {
    5: 126,
    7: 126,
    9: 1778,
    11: 6510,
    13: 23622,
    15: 510,
    17: 507842,
    19: 1523526,
    21: 8388606,
}


def addCandidate(heap, counts, value):
    counts[value] += 1
    heapq.heappush(heap, value)


def popUnique(heap, counts, odd_only=False):
    while heap:
        value = heapq.heappop(heap)
        count = counts[value]
        if count == 0:
            continue

        counts[value] = 0
        if count == 1 and (not odd_only or value % 2 == 1):
            return value

    raise ValueError("No candidate available")


def initializeSequence(second_start):
    sequence = [2, second_start]
    heap = []
    counts = collections.Counter()
    addCandidate(heap, counts, 2 + second_start)
    even_count = 1
    second_even_index = None

    while second_even_index is None:
        value = popUnique(heap, counts)
        sequence.append(value)

        if value % 2 == 0:
            even_count += 1
            if even_count == 2:
                second_even_index = len(sequence) - 1

        for previous in sequence[:-1]:
            addCandidate(heap, counts, previous + value)

    return sequence, heap, counts, second_even_index


def ulamPrefix(second_start, length):
    sequence, heap, counts, second_even_index = initializeSequence(second_start)

    while len(sequence) < length:
        last = sequence[-1]
        addCandidate(heap, counts, sequence[0] + last)
        addCandidate(heap, counts, sequence[second_even_index] + last)
        sequence.append(popUnique(heap, counts, odd_only=True))

    return sequence, second_even_index


def ulamValue(second_start, index):
    period = PERIODS[second_start]
    difference = FUNDAMENTAL_DIFFERENCES[second_start]
    sequence, second_even_index = ulamPrefix(second_start, period + 50)
    required_length = second_even_index + period + 2

    if len(sequence) < required_length:
        sequence, second_even_index = ulamPrefix(second_start, required_length)

    prefix_length = second_even_index + 1
    if index <= prefix_length:
        return sequence[index - 1]

    shifted_index = index - prefix_length
    remainder = shifted_index % period
    if remainder == 0:
        remainder = period

    return (
        sequence[second_even_index + remainder]
        + ((shifted_index - remainder) // period) * difference
    )


def ulamSum(index):
    return sum(ulamValue(second_start, index) for second_start in range(5, 22, 2))


def runTests():
    assert [ulamValue(5, index) for index in range(1, 11)] == [2, 5, 7, 9, 11, 12, 13, 15, 19, 23]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ulamSum(10 ** 11)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
