from bisect import bisect_right
from collections import deque
import math
import time


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"

    for p in range(2, int(limit**0.5) + 1):
        if isPrime[p]:
            start = p * p
            isPrime[start:limit + 1:p] = b"\x00" * (((limit - start) // p) + 1)

    return [n for n in range(2, limit + 1) if isPrime[n]]


def integerCubeRoot(n):
    root = int(round(n ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= n:
        root += 1
    while root**3 > n:
        root -= 1
    return root


def kahanSum(values):
    total = 0.0
    correction = 0.0

    for value in values:
        adjusted = value - correction
        nextTotal = total + adjusted
        correction = (nextTotal - total) - adjusted
        total = nextTotal

    return total


class Dinic:
    def __init__(self, size):
        self.size = size
        self.graph = [[] for _ in range(size)]

    def addEdge(self, start, end, capacity):
        forward = [end, capacity, len(self.graph[end])]
        backward = [start, 0, len(self.graph[start])]
        self.graph[start].append(forward)
        self.graph[end].append(backward)

    def maxFlow(self, source, sink):
        flow = 0
        level = [-1] * self.size

        def bfs():
            for i in range(self.size):
                level[i] = -1
            level[source] = 0
            queue = deque([source])

            while queue:
                node = queue.popleft()
                for target, capacity, _ in self.graph[node]:
                    if capacity > 0 and level[target] < 0:
                        level[target] = level[node] + 1
                        queue.append(target)

            return level[sink] >= 0

        def dfs(node, amount):
            if node == sink:
                return amount

            for index in range(iterator[node], len(self.graph[node])):
                iterator[node] = index
                edge = self.graph[node][index]
                target, capacity, reverseIndex = edge
                if capacity > 0 and level[target] == level[node] + 1:
                    pushed = dfs(target, min(amount, capacity))
                    if pushed:
                        edge[1] -= pushed
                        self.graph[target][reverseIndex][1] += pushed
                        return pushed

            return 0

        while bfs():
            iterator = [0] * self.size
            while True:
                pushed = dfs(source, 10**30)
                if not pushed:
                    break
                flow += pushed

        return flow

    def reachableFrom(self, source):
        seen = [False] * self.size
        seen[source] = True
        queue = deque([source])

        while queue:
            node = queue.popleft()
            for target, capacity, _ in self.graph[node]:
                if capacity > 0 and not seen[target]:
                    seen[target] = True
                    queue.append(target)

        return seen


def forcedPrimes(primes, limit):
    forced = {prime for prime in primes if prime % 10 == 3}
    cubeRoot = integerCubeRoot(limit)
    forced.update(prime for prime in primes if prime % 10 == 7 and prime <= cubeRoot)
    return forced


def buildPrefixGraph(primes, limit, forced):
    left = [
        prime
        for prime in primes
        if prime % 10 == 7 and prime not in forced and prime * 19 <= limit
    ]
    left.sort()
    if not left:
        return [], [], []

    right = [
        prime
        for prime in primes
        if prime % 10 == 9 and prime <= limit // left[0]
    ]
    right.sort()
    prefixLengths = [bisect_right(right, limit // prime) for prime in left]
    return left, right, prefixLengths


def minimumWeightVertexCover(left, right, prefixLengths):
    scale = 10**12
    leftWeights = [int(round(math.log(prime) * scale)) for prime in left]
    rightWeights = [int(round(math.log(prime) * scale)) for prime in right]
    infiniteCapacity = sum(leftWeights) + sum(rightWeights) + 1

    source = 0
    leftOffset = 1
    rightOffset = 1 + len(left)
    sink = 1 + len(left) + len(right)
    flow = Dinic(sink + 1)

    for i, weight in enumerate(leftWeights):
        flow.addEdge(source, leftOffset + i, weight)
    for i, weight in enumerate(rightWeights):
        flow.addEdge(rightOffset + i, sink, weight)

    for i, prefixLength in enumerate(prefixLengths):
        node = leftOffset + i
        for j in range(prefixLength):
            flow.addEdge(node, rightOffset + j, infiniteCapacity)

    flow.maxFlow(source, sink)
    reachable = flow.reachableFrom(source)

    coverLeft = {
        prime
        for i, prime in enumerate(left)
        if not reachable[leftOffset + i]
    }
    coverRight = {
        prime
        for i, prime in enumerate(right)
        if reachable[rightOffset + i]
    }
    return coverLeft, coverRight


def lnF(limit, returnPrimes=False):
    primes = primeSieve(limit)
    forced = forcedPrimes(primes, limit)
    left, right, prefixLengths = buildPrefixGraph(primes, limit, forced)

    coverLeft = set()
    coverRight = set()
    if left and right:
        coverLeft, coverRight = minimumWeightVertexCover(left, right, prefixLengths)

    chosen = forced | coverLeft | coverRight
    logValue = kahanSum(math.log(prime) for prime in sorted(chosen))

    if returnPrimes:
        return logValue, chosen
    return logValue


def runTests():
    log40, primes40 = lnF(40, returnPrimes=True)
    product = 1
    for prime in primes40:
        product *= prime

    assert product == 897
    assert format(log40, ".6f") == "6.799056"
    assert format(lnF(2800), ".6f") == "715.019337"


def solve():
    return format(lnF(10**6), ".6f")


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
