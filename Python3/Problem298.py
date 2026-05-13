import time
from collections import defaultdict
from decimal import Decimal, getcontext


TURNS = 50
NUMBER_COUNT = 10
MEMORY_SIZE = 5


def canonicalMemories(larry_memory, robin_memory):
    mapping = {}
    next_label = 0
    result = []

    for memory in (larry_memory, robin_memory):
        canonical = []
        for number in memory:
            if number not in mapping:
                mapping[number] = next_label
                next_label += 1
            canonical.append(mapping[number])
        result.append(tuple(canonical))

    return result[0], result[1], next_label


def larryStep(memory, number):
    memory = list(memory)
    score = 0

    if number in memory:
        score = 1
        memory.remove(number)
    elif len(memory) == MEMORY_SIZE:
        memory.pop(0)

    memory.append(number)
    return tuple(memory), score


def robinStep(memory, number):
    memory = list(memory)
    score = 0

    if number in memory:
        score = 1
    else:
        if len(memory) == MEMORY_SIZE:
            memory.pop(0)
        memory.append(number)

    return tuple(memory), score


def expectedAbsoluteScoreDifference(turns):
    states = {((), (), 0): 1}

    for _ in range(turns):
        next_states = defaultdict(int)

        for (larry_memory, robin_memory, difference), count in states.items():
            used_labels = max(larry_memory + robin_memory, default=-1) + 1

            for number in range(used_labels):
                next_larry, larry_score = larryStep(larry_memory, number)
                next_robin, robin_score = robinStep(robin_memory, number)
                next_larry, next_robin, _used = canonicalMemories(
                    next_larry, next_robin
                )
                next_states[
                    (next_larry, next_robin, difference + larry_score - robin_score)
                ] += count

            new_number_count = NUMBER_COUNT - used_labels
            if new_number_count:
                number = used_labels
                next_larry, larry_score = larryStep(larry_memory, number)
                next_robin, robin_score = robinStep(robin_memory, number)
                next_larry, next_robin, _used = canonicalMemories(
                    next_larry, next_robin
                )
                next_states[
                    (next_larry, next_robin, difference + larry_score - robin_score)
                ] += count * new_number_count

        states = next_states

    numerator = sum(
        abs(difference) * count for (_larry, _robin, difference), count in states.items()
    )

    getcontext().prec = 30
    return Decimal(numerator) / (Decimal(NUMBER_COUNT) ** turns)


def bruteExpectedAbsoluteScoreDifference(turns):
    states = {((), (), 0): 1}

    for _ in range(turns):
        next_states = defaultdict(int)

        for (larry_memory, robin_memory, difference), count in states.items():
            for number in range(1, NUMBER_COUNT + 1):
                next_larry, larry_score = larryStep(larry_memory, number)
                next_robin, robin_score = robinStep(robin_memory, number)
                next_states[
                    (next_larry, next_robin, difference + larry_score - robin_score)
                ] += count

        states = next_states

    numerator = sum(
        abs(difference) * count for (_larry, _robin, difference), count in states.items()
    )
    getcontext().prec = 30
    return Decimal(numerator) / (Decimal(NUMBER_COUNT) ** turns)


def runTests():
    assert expectedAbsoluteScoreDifference(1) == Decimal(0)
    assert expectedAbsoluteScoreDifference(6) == bruteExpectedAbsoluteScoreDifference(6)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = expectedAbsoluteScoreDifference(TURNS).quantize(Decimal("0.00000001"))
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
