import hashlib
import time
from collections import deque
from functools import lru_cache


TARGET_INDEX = 10**18
TARGET_MD5 = "c31bb13db787bce9a169dce600aec863"


def forbiddenPatterns(maxLength=25):
    patterns = []
    value = 11

    while len(str(value)) <= maxLength:
        patterns.append(str(value))
        value *= 11

    return patterns


def buildAutomaton():
    trie = [{}]
    failure = [0]
    forbidden = [False]

    for pattern in forbiddenPatterns():
        state = 0

        for digit in pattern:
            if digit not in trie[state]:
                trie[state][digit] = len(trie)
                trie.append({})
                failure.append(0)
                forbidden.append(False)

            state = trie[state][digit]

        forbidden[state] = True

    queue = deque(trie[0].values())

    while queue:
        state = queue.popleft()
        forbidden[state] = forbidden[state] or forbidden[failure[state]]

        for digit, nextState in trie[state].items():
            fallback = failure[state]

            while fallback and digit not in trie[fallback]:
                fallback = failure[fallback]

            failure[nextState] = trie[fallback].get(digit, 0)
            queue.append(nextState)

    transitions = [[0] * 10 for _ in trie]

    for state in range(len(trie)):
        for digit in range(10):
            character = str(digit)
            fallback = state

            while fallback and character not in trie[fallback]:
                fallback = failure[fallback]

            transitions[state][digit] = trie[fallback].get(character, 0)

    return transitions, forbidden


TRANSITIONS, FORBIDDEN = buildAutomaton()


@lru_cache(maxsize=None)
def countCompletions(state, remaining):
    if remaining == 0:
        return 1

    total = 0

    for digit in range(10):
        nextState = TRANSITIONS[state][digit]

        if not FORBIDDEN[nextState]:
            total += countCompletions(nextState, remaining - 1)

    return total


def countLength(length):
    total = 0

    for digit in range(1, 10):
        state = TRANSITIONS[0][digit]

        if not FORBIDDEN[state]:
            total += countCompletions(state, length - 1)

    return total


def elevenFree(index):
    total = 0
    length = 1

    while total + countLength(length) < index:
        total += countLength(length)
        length += 1

    rank = index - total
    state = 0
    digits = []

    for position in range(length):
        for digit in range(1 if position == 0 else 0, 10):
            nextState = TRANSITIONS[state][digit]

            if FORBIDDEN[nextState]:
                continue

            count = countCompletions(nextState, length - position - 1)

            if rank > count:
                rank -= count
            else:
                digits.append(str(digit))
                state = nextState
                break

    return int("".join(digits))


def runTests():
    assert elevenFree(3) == 3
    assert elevenFree(200) == 213
    assert elevenFree(500_000) == 531563
    assert hashlib.md5(str(elevenFree(TARGET_INDEX)).encode()).hexdigest() == TARGET_MD5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = elevenFree(TARGET_INDEX)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
