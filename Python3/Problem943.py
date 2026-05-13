import time


TARGET = 22_332_223_332_233
MODULUS = 2_233_222_333
MAX_SYMBOL = 223


class Result:
    __slots__ = ("countA", "countB", "nextState", "total")

    def __init__(self, countA, countB, nextState):
        self.countA = countA
        self.countB = countB
        self.nextState = nextState
        self.total = countA + countB


class KolakoskiCounter:
    def __init__(self, a, b, limit):
        self.a = a
        self.b = b
        self.limit = limit
        self.overflow = limit + 1
        self.cache = {}

    def runLength(self, state, level):
        return self.b if state & (2 << level) else self.a

    def fullBlock(self, state, level):
        key = state + (4 << level)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        runLength = self.runLength(state, level)
        if level == 0:
            if state & 1:
                result = Result(0, runLength, state ^ 1)
            else:
                result = Result(runLength, 0, state ^ 1)
            self.cache[key] = result
            return result

        bit = state & (2 << level)
        substate = state ^ bit
        countA = 0
        countB = 0

        for _ in range(runLength):
            child = self.fullBlock(substate, level - 1)
            if child.total > self.limit - countA - countB:
                result = Result(self.overflow, 0, substate)
                self.cache[key] = result
                return result
            countA += child.countA
            countB += child.countB
            substate = child.nextState

        result = Result(countA, countB, substate ^ bit ^ (1 << level))
        self.cache[key] = result
        return result

    def prefixBlock(self, state, level, maxLength):
        if maxLength <= 0:
            return Result(0, 0, state)

        runLength = self.runLength(state, level)
        if level == 0:
            count = min(runLength, maxLength)
            if state & 1:
                return Result(0, count, state ^ 1)
            return Result(count, 0, state ^ 1)

        bit = state & (2 << level)
        substate = state ^ bit
        countA = 0
        countB = 0
        produced = 0

        for _ in range(runLength):
            remaining = maxLength - produced
            if remaining <= 0:
                break

            child = self.fullBlock(substate, level - 1)
            if child.total <= remaining:
                current = child
            else:
                current = self.prefixBlock(substate, level - 1, remaining)

            countA += current.countA
            countB += current.countB
            produced += current.total
            substate = current.nextState

            if produced >= maxLength:
                break

        return Result(countA, countB, substate ^ bit ^ (1 << level))

    def counts(self):
        level = 0
        while self.fullBlock(0, level).total < self.limit:
            level += 1

        return self.prefixBlock(0, level, self.limit)


def T(a, b, limit):
    counts = KolakoskiCounter(a, b, limit).counts()
    return a * counts.countA + b * counts.countB


def solve():
    total = 0
    for a in range(2, MAX_SYMBOL + 1):
        for b in range(2, MAX_SYMBOL + 1):
            if a != b:
                total = (total + T(a, b, TARGET)) % MODULUS
    return total


def runTests():
    assert T(2, 3, 10) == 25
    assert T(4, 2, 10_000) == 30_004
    assert T(5, 8, 1_000_000) == 6_499_871


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
