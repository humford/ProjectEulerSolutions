import bisect
import heapq
import math
import time


LEAF = None
PRIMALITY_CACHE = {}
FACTOR_CACHE = {}
BEST_DIVISOR_CACHE = {}
SHAPE_CACHE = {}
SEQUENCES = {}


def isPrime(n):
    if n in PRIMALITY_CACHE:
        return PRIMALITY_CACHE[n]
    if n < 2:
        PRIMALITY_CACHE[n] = False
        return False

    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == prime:
            PRIMALITY_CACHE[n] = True
            return True
        if n % prime == 0:
            PRIMALITY_CACHE[n] = False
            return False

    oddPart = n - 1
    shifts = 0
    while oddPart % 2 == 0:
        oddPart //= 2
        shifts += 1

    for witness in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if witness % n == 0:
            continue
        x = pow(witness, oddPart, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            PRIMALITY_CACHE[n] = False
            return False

    PRIMALITY_CACHE[n] = True
    return True


def pollardRhoBrent(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    for c in (1, 3, 5, 7, 11, 13, 17, 19, 23):
        y = 2
        block = 128
        gcdValue = 1
        r = 1
        q = 1

        def f(x):
            return (x * x + c) % n

        while gcdValue == 1:
            x = y
            for _ in range(r):
                y = f(y)
            k = 0
            while k < r and gcdValue == 1:
                ys = y
                for _ in range(min(block, r - k)):
                    y = f(y)
                    q = q * abs(x - y) % n
                gcdValue = math.gcd(q, n)
                k += block
            r <<= 1

        if gcdValue == n:
            gcdValue = 1
            y = ys
            while gcdValue == 1:
                y = f(y)
                gcdValue = math.gcd(abs(x - y), n)

        if 1 < gcdValue < n:
            return gcdValue

    divisor = 5
    while divisor <= math.isqrt(n) and divisor <= 1_000_000:
        if n % divisor == 0:
            return divisor
        divisor += 2
    return n


def factorize(n):
    if n in FACTOR_CACHE:
        return dict(FACTOR_CACHE[n])

    original = n
    factors = {}
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % prime == 0:
            exponent = 0
            while n % prime == 0:
                n //= prime
                exponent += 1
            factors[prime] = factors.get(prime, 0) + exponent

    def recurse(value):
        if value == 1:
            return
        if isPrime(value):
            factors[value] = factors.get(value, 0) + 1
            return
        divisor = pollardRhoBrent(value)
        if divisor == value:
            factors[value] = factors.get(value, 0) + 1
            return
        recurse(divisor)
        recurse(value // divisor)

    if n > 1:
        recurse(n)

    FACTOR_CACHE[original] = dict(factors)
    return dict(factors)


def productsFromFactors(items):
    result = [1]
    for prime, exponent in items:
        powers = [1]
        value = 1
        for _ in range(exponent):
            value *= prime
            powers.append(value)
        result = [base * power for base in result for power in powers]
    return result


def bestDivisorAtMostSqrt(n):
    if n in BEST_DIVISOR_CACHE:
        return BEST_DIVISOR_CACHE[n]

    items = sorted(factorize(n).items())
    split = len(items) // 2
    leftDivisors = productsFromFactors(items[:split])
    rightDivisors = sorted(productsFromFactors(items[split:]))
    root = math.isqrt(n)
    best = 1

    for left in leftDivisors:
        if left > root:
            continue
        index = bisect.bisect_right(rightDivisors, root // left) - 1
        if index >= 0:
            best = max(best, left * rightDivisors[index])

    BEST_DIVISOR_CACHE[n] = best
    return best


def shapeOf(n):
    if n in SHAPE_CACHE:
        return SHAPE_CACHE[n]
    if isPrime(n):
        SHAPE_CACHE[n] = LEAF
        return LEAF

    left = bestDivisorAtMostSqrt(n)
    right = n // left
    shape = (shapeOf(left), shapeOf(right))
    SHAPE_CACHE[n] = shape
    return shape


def doubleFactorial(n):
    result = 1
    for value in range(n, 1, -2):
        result *= value
    return result


def leafCount(shape):
    if shape is LEAF:
        return 1
    return leafCount(shape[0]) + leafCount(shape[1])


class ShapeSequence:
    def __init__(self, shape, maxValue):
        self.shape = shape
        self.maxValue = maxValue
        self.values = []

        if shape is LEAF:
            self.kind = "leaf"
            self.nextPrime = 2
        else:
            self.kind = "node"
            self.left = shape[0]
            self.right = shape[1]
            self.heap = []
            self.inHeap = set()
            self.nextLeftIndex = 0
            self.started = False

    def yieldNextPrime(self):
        if self.nextPrime > self.maxValue:
            raise StopIteration
        if self.nextPrime == 2:
            self.nextPrime = 3
            return 2

        candidate = self.nextPrime
        while candidate <= self.maxValue:
            if isPrime(candidate):
                self.nextPrime = candidate + 2
                return candidate
            candidate += 2

        raise StopIteration

    def tryValue(self, shape, index):
        try:
            return getValue(shape, index)
        except StopIteration:
            return None

    def ensureRightAtLeast(self, value):
        sequence = SEQUENCES[self.right]
        if not sequence.values:
            try:
                sequence.values.append(sequence.nextValue())
            except StopIteration:
                return None

        while sequence.values[-1] < value:
            try:
                nextValue = sequence.nextValue()
            except StopIteration:
                break
            if nextValue > self.maxValue:
                break
            sequence.values.append(nextValue)

        if sequence.values[-1] < value:
            return None
        return bisect.bisect_left(sequence.values, value)

    def pushPair(self, i, j):
        if (i, j) in self.inHeap:
            return
        leftValue = self.tryValue(self.left, i)
        rightValue = self.tryValue(self.right, j)
        if leftValue is None or rightValue is None or leftValue > rightValue:
            return
        product = leftValue * rightValue
        if product > self.maxValue:
            return
        self.inHeap.add((i, j))
        heapq.heappush(self.heap, (product, i, j))

    def startNode(self):
        if self.started:
            return
        self.started = True
        leftValue = self.tryValue(self.left, 0)
        if leftValue is None:
            return
        rightIndex = self.ensureRightAtLeast(leftValue)
        if rightIndex is not None:
            self.pushPair(0, rightIndex)
        self.nextLeftIndex = 1

    def maybeAddLeftLists(self, currentMinimum):
        while True:
            leftValue = self.tryValue(self.left, self.nextLeftIndex)
            if leftValue is None:
                return
            if self.heap and leftValue * leftValue > currentMinimum:
                return
            rightIndex = self.ensureRightAtLeast(leftValue)
            if rightIndex is not None:
                self.pushPair(self.nextLeftIndex, rightIndex)
            self.nextLeftIndex += 1

    def nextCandidateProduct(self):
        self.startNode()

        while True:
            if not self.heap:
                leftValue = self.tryValue(self.left, self.nextLeftIndex)
                if leftValue is None:
                    raise StopIteration
                rightIndex = self.ensureRightAtLeast(leftValue)
                if rightIndex is None:
                    raise StopIteration
                self.pushPair(self.nextLeftIndex, rightIndex)
                self.nextLeftIndex += 1
                continue

            product, i, j = heapq.heappop(self.heap)
            self.maybeAddLeftLists(product)
            self.pushPair(i, j + 1)
            return product

    def nextValue(self):
        if self.kind == "leaf":
            return self.yieldNextPrime()

        previous = self.values[-1] if self.values else None
        while True:
            candidate = self.nextCandidateProduct()
            if previous is not None and candidate == previous:
                continue
            if shapeOf(candidate) == self.shape:
                return candidate


def getValue(shape, index):
    sequence = SEQUENCES[shape]
    while len(sequence.values) <= index:
        sequence.values.append(sequence.nextValue())
    return sequence.values[index]


def collectShapes(shape, collected):
    if shape in collected:
        return
    collected.add(shape)
    if shape is not LEAF:
        collectShapes(shape[0], collected)
        collectShapes(shape[1], collected)


def M(n):
    maxValue = doubleFactorial(31)
    targetShape = shapeOf(doubleFactorial(n))
    shapes = set()
    collectShapes(targetShape, shapes)

    for shape in sorted(shapes, key=leafCount):
        if shape not in SEQUENCES:
            SEQUENCES[shape] = ShapeSequence(shape, maxValue)

    return getValue(targetShape, 0)


def solve():
    maxValue = doubleFactorial(31)
    targetShapes = [shapeOf(doubleFactorial(n)) for n in range(2, 32)]
    allShapes = set()
    for shape in targetShapes:
        collectShapes(shape, allShapes)

    SEQUENCES.clear()
    for shape in sorted(allShapes, key=leafCount):
        SEQUENCES[shape] = ShapeSequence(shape, maxValue)

    values = [getValue(shape, 0) for shape in targetShapes]
    assert values[7] == 72
    return sum(values)


def runTests():
    assert M(9) == 72


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
