import time


def canReach(target, max_depth):
    chain = [1]

    def search():
        depth = len(chain) - 1
        current = chain[-1]
        remaining = max_depth - depth

        if depth == max_depth:
            return current == target
        if current << remaining < target:
            return False

        candidates = set()
        for value in reversed(chain):
            candidate = current + value
            if current < candidate <= target:
                candidates.add(candidate)

        for candidate in sorted(candidates, reverse=True):
            chain.append(candidate)
            if search():
                return True
            chain.pop()

        return False

    return search()


def minimalMultiplications(exponent):
    if exponent == 1:
        return 0

    depth = 1
    while not canReach(exponent, depth):
        depth += 1
    return depth


def sumMinimalMultiplications(limit):
    return sum(minimalMultiplications(exponent) for exponent in range(1, limit + 1))


def runTests():
    assert minimalMultiplications(1) == 0
    assert minimalMultiplications(15) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumMinimalMultiplications(200)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
