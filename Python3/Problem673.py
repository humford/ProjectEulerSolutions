import math
import time
from collections import defaultdict


MODULUS = 999_999_937


def readPairs(path):
    pairs = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                a, b = stripped.split(",")
                pairs.append((int(a), int(b)))
    return pairs


def makeInvolution(size, pairs):
    involution = list(range(size + 1))
    for a, b in pairs:
        involution[a] = b
        involution[b] = a
    return involution


def classifyComponent(component, bed, desk):
    hasLoop = any(bed[student] == student or desk[student] == student
                  for student in component)
    size = len(component)

    if not hasLoop:
        return ("cycle", size), size

    if size % 2 == 1:
        return ("path", size, "mixed"), 1

    endpointLoop = None
    for student in component:
        if bed[student] == student and desk[student] != student:
            endpointLoop = "bed"
            break
        if desk[student] == student and bed[student] != student:
            endpointLoop = "desk"
            break

    return ("path", size, endpointLoop), 2


def validPermutationCount(size, bedPairs, deskPairs, modulus=MODULUS):
    bed = makeInvolution(size, bedPairs)
    desk = makeInvolution(size, deskPairs)

    visited = [False] * (size + 1)
    typeCounts = defaultdict(int)
    automorphismCounts = {}

    for start in range(1, size + 1):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        component = []
        while stack:
            student = stack.pop()
            component.append(student)
            for neighbour in (bed[student], desk[student]):
                if not visited[neighbour]:
                    visited[neighbour] = True
                    stack.append(neighbour)

        componentType, automorphisms = classifyComponent(component, bed, desk)
        typeCounts[componentType] += 1
        automorphismCounts[componentType] = automorphisms

    total = 1
    for componentType, count in typeCounts.items():
        total *= pow(automorphismCounts[componentType], count, modulus)
        total *= math.factorial(count)
        total %= modulus

    return total


def downloadedFilePermutationCount():
    return validPermutationCount(
        500,
        readPairs("Files/p673_beds.txt"),
        readPairs("Files/p673_desks.txt"),
    )


def runTests():
    assert validPermutationCount(4, [(2, 3)], [(1, 3), (2, 4)]) == 2
    assert validPermutationCount(
        6,
        [(1, 2), (3, 4), (5, 6)],
        [(3, 6), (4, 5)],
    ) == 8
    assert validPermutationCount(
        36,
        [
            (2, 13), (4, 30), (5, 27), (6, 16), (10, 18),
            (12, 35), (14, 19), (15, 20), (17, 26), (21, 32),
            (22, 33), (24, 34), (25, 28),
        ],
        [
            (1, 35), (2, 22), (3, 36), (4, 28), (5, 25),
            (7, 18), (9, 23), (13, 19), (14, 33), (15, 34),
            (20, 24), (26, 29), (27, 30),
        ],
    ) == 663_552


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = downloadedFilePermutationCount()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
