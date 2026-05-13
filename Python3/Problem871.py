from collections import deque
import time


START_N = 10**5 + 1
END_N = 10**5 + 100


def functionValues(n):
    return [((x * x % n) * x + x + 1) % n for x in range(n)]


def maxPathMatching(weights):
    skip = 0
    take = -10**18

    for weight in weights:
        skip, take = max(skip, take), skip + weight

    return max(skip, take)


def maxCycleMatching(weights):
    length = len(weights)
    if length == 1:
        return 0
    if length == 2:
        return max(0, weights[0])

    withoutWrap = maxPathMatching(weights[:-1])
    withWrap = weights[-1] + maxPathMatching(weights[1:-2])
    return max(withoutWrap, withWrap, 0)


def treeDp(children, node, dpFree, dpBlocked):
    blocked = 0
    bestGain = 0

    for child in children[node]:
        blocked += dpFree[child]
        bestGain = max(bestGain, 1 + dpBlocked[child] - dpFree[child])

    dpBlocked[node] = blocked
    dpFree[node] = blocked + bestGain


def D(n):
    successor = functionValues(n)
    indegree = [0] * n
    for target in successor:
        indegree[target] += 1

    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    removedOrder = []
    while queue:
        node = queue.popleft()
        removedOrder.append(node)
        target = successor[node]
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)

    isCycle = [degree > 0 for degree in indegree]
    children = [[] for _ in range(n)]
    for node, target in enumerate(successor):
        if node == target:
            continue
        if isCycle[node] and isCycle[target]:
            continue
        children[target].append(node)

    dpFree = [0] * n
    dpBlocked = [0] * n
    for node in removedOrder:
        treeDp(children, node, dpFree, dpBlocked)

    total = 0
    visitedCycle = [False] * n

    for start in range(n):
        if not isCycle[start] or visitedCycle[start]:
            continue

        cycle = []
        node = start
        while not visitedCycle[node]:
            visitedCycle[node] = True
            cycle.append(node)
            node = successor[node]

        for node in cycle:
            treeDp(children, node, dpFree, dpBlocked)

        total += sum(dpFree[node] for node in cycle)

        if len(cycle) > 1:
            edgeWeights = []
            for i, node in enumerate(cycle):
                nextNode = cycle[(i + 1) % len(cycle)]
                edgeWeights.append(
                    1
                    + dpBlocked[node]
                    - dpFree[node]
                    + dpBlocked[nextNode]
                    - dpFree[nextNode]
                )
            total += maxCycleMatching(edgeWeights)

    return total


def bruteD(n):
    successor = functionValues(n)
    best = 0

    for mask in range(1 << n):
        chosen = [i for i in range(n) if (mask >> i) & 1]
        images = [successor[i] for i in chosen]
        if len(set(images)) != len(images):
            continue
        if set(chosen) & set(images):
            continue
        best = max(best, len(chosen))

    return best


def solve():
    return sum(D(n) for n in range(START_N, END_N + 1))


def runTests():
    assert D(5) == 1
    assert D(10) == 3
    for n in range(1, 13):
        assert D(n) == bruteD(n)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
