from array import array
from collections import deque
import time


MODULUS = 1_001_001_011


def buildSuccessorAndIndegree(bits):
    stateCount = 1 << bits
    successors = array("I", [0]) * stateCount
    indegrees = array("I", [0]) * stateCount
    mask = (1 << (bits - 1)) - 1
    shift = bits - 3

    for state in range(stateCount):
        firstThree = state >> shift
        b1 = (firstThree >> 2) & 1
        b2 = (firstThree >> 1) & 1
        b3 = firstThree & 1
        nextBit = b1 & (b2 ^ b3)
        successor = ((state & mask) << 1) | nextBit
        successors[state] = successor
        indegrees[successor] += 1

    return successors, indegrees


def circularLogicCount(bits, modulus=MODULUS):
    if bits < 3:
        raise ValueError("bits must be at least 3")

    stateCount = 1 << bits
    successors, indegrees = buildSuccessorAndIndegree(bits)
    acc0 = array("I", [1]) * stateCount
    acc1 = array("I", [1]) * stateCount
    inCycle = bytearray(b"\x01") * stateCount
    queue = deque()

    for state in range(stateCount):
        if indegrees[state] == 0:
            queue.append(state)

    while queue:
        state = queue.popleft()
        if inCycle[state] == 0:
            continue

        inCycle[state] = 0
        parent = successors[state]
        dp0 = acc0[state]
        dp1 = acc1[state]

        acc0[parent] = acc0[parent] * ((dp0 + dp1) % modulus) % modulus
        acc1[parent] = acc1[parent] * dp0 % modulus

        indegrees[parent] -= 1
        if indegrees[parent] == 0:
            queue.append(parent)

    visited = bytearray(stateCount)
    answer = 1

    for start in range(stateCount):
        if not inCycle[start] or visited[start]:
            continue

        cycle = []
        state = start
        while not visited[state]:
            visited[state] = 1
            cycle.append(state)
            state = successors[state]

        weights0 = [int(acc0[state]) % modulus for state in cycle]
        weights1 = [int(acc1[state]) % modulus for state in cycle]

        previous0 = weights0[0]
        previous1 = 0
        for i in range(1, len(cycle)):
            current0 = (previous0 + previous1) * weights0[i] % modulus
            current1 = previous0 * weights1[i] % modulus
            previous0, previous1 = current0, current1
        firstNotChosen = (previous0 + previous1) % modulus

        previous0 = 0
        previous1 = weights1[0]
        for i in range(1, len(cycle)):
            current0 = (previous0 + previous1) * weights0[i] % modulus
            current1 = previous0 * weights1[i] % modulus
            previous0, previous1 = current0, current1
        firstChosen = previous0

        answer = answer * ((firstNotChosen + firstChosen) % modulus) % modulus

    return answer


def runTests():
    assert circularLogicCount(3) == 35
    assert circularLogicCount(4) == 2_118


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = circularLogicCount(20)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
