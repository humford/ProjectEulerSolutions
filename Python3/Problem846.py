from collections import deque
import math
import sys
import time


def primeSieve(limit):
    if limit < 2:
        return []

    isPrime = bytearray(b"\x01") * (limit + 1)
    isPrime[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if isPrime[p]:
            isPrime[p * p:limit + 1:p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [n for n in range(2, limit + 1) if isPrime[n]]


def tonelliShanks(n, prime):
    n %= prime
    if n == 0:
        return 0
    if prime == 2:
        return n
    if pow(n, (prime - 1) // 2, prime) != 1:
        raise ValueError("not a quadratic residue")
    if prime % 4 == 3:
        return pow(n, (prime + 1) // 4, prime)

    q = prime - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while pow(z, (prime - 1) // 2, prime) != prime - 1:
        z += 1

    m = s
    c = pow(z, q, prime)
    t = pow(n, q, prime)
    x = pow(n, (q + 1) // 2, prime)

    while t != 1:
        i = 1
        t2i = t * t % prime
        while i < m and t2i != 1:
            t2i = t2i * t2i % prime
            i += 1

        b = pow(c, 1 << (m - i - 1), prime)
        x = x * b % prime
        t = t * b * b % prime
        c = b * b % prime
        m = i

    return x


def buildGraph(limit):
    primes = primeSieve(limit)
    allowed = {1, 2}
    oddNodes = [1]
    rootMod = {}

    for prime in primes:
        if prime % 4 != 1:
            continue

        root = tonelliShanks(prime - 1, prime)
        root = min(root, prime - root)
        primePower = prime
        currentRoot = root

        while primePower <= limit:
            allowed.add(primePower)
            oddNodes.append(primePower)
            rootMod[primePower] = currentRoot
            if 2 * primePower <= limit:
                allowed.add(2 * primePower)

            nextPrimePower = primePower * prime
            if nextPrimePower > limit:
                break

            quotient = ((currentRoot * currentRoot + 1) // primePower) % prime
            inverse = pow((2 * currentRoot) % prime, -1, prime)
            delta = -quotient * inverse % prime
            currentRoot += delta * primePower
            primePower = nextPrimePower

    adjacency = {}

    def addEdge(a, b):
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)

    for a in oddNodes:
        if a == 1:
            limitX = math.isqrt(limit - 1)
            for x in range(1, limitX + 1):
                b = x * x + 1
                if b in allowed and b != 1:
                    addEdge(1, b)
            continue

        root = rootMod[a]
        limitX = math.isqrt(a * limit - 1)
        for residue in (root, a - root):
            for x in range(residue, limitX + 1, a):
                b = (x * x + 1) // a
                if b != a and b <= limit and b in allowed:
                    addEdge(a, b)

    return adjacency


def inducedSubgraph(fullAdjacency, limit):
    adjacency = {}
    for vertex, neighbors in fullAdjacency.items():
        if vertex <= limit:
            filtered = {neighbor for neighbor in neighbors if neighbor <= limit}
            if filtered:
                adjacency[vertex] = filtered
    return adjacency


def pruneToTwoCore(adjacency):
    degree = {vertex: len(neighbors) for vertex, neighbors in adjacency.items()}
    queue = deque([vertex for vertex, value in degree.items() if value < 2])
    removed = set()

    while queue:
        vertex = queue.popleft()
        if vertex in removed:
            continue
        removed.add(vertex)

        for neighbor in list(adjacency.get(vertex, ())):
            adjacency[neighbor].remove(vertex)
            degree[neighbor] -= 1
            if degree[neighbor] < 2 and neighbor not in removed:
                queue.append(neighbor)
        adjacency[vertex].clear()

    for vertex in list(adjacency):
        if not adjacency[vertex]:
            del adjacency[vertex]


def biconnectedComponents(adjacency):
    sys.setrecursionlimit(1_000_000)
    discovery = {}
    low = {}
    parent = {}
    edgeStack = []
    components = []
    timer = 0

    def dfs(vertex):
        nonlocal timer
        timer += 1
        discovery[vertex] = low[vertex] = timer

        for neighbor in adjacency[vertex]:
            if neighbor not in discovery:
                parent[neighbor] = vertex
                edgeStack.append((vertex, neighbor))
                dfs(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])

                if low[neighbor] >= discovery[vertex]:
                    component = []
                    while True:
                        edge = edgeStack.pop()
                        component.append(edge)
                        if edge == (vertex, neighbor):
                            break
                    components.append(component)
            elif parent.get(vertex) != neighbor and discovery[neighbor] < discovery[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbor])
                edgeStack.append((vertex, neighbor))

    for vertex in adjacency:
        if vertex not in discovery:
            dfs(vertex)
            if edgeStack:
                components.append(list(edgeStack))
                edgeStack.clear()

    return components


def cycleSumInBlock(blockAdjacency):
    nodes = sorted(blockAdjacency)
    neighbors = {node: sorted(blockAdjacency[node]) for node in nodes}
    total = 0

    def dfs(start, current, first, visited, pathSum, pathLength):
        nonlocal total
        for nextNode in neighbors[current]:
            if nextNode == start:
                if pathLength >= 3 and first < current:
                    total += pathSum
                continue
            if nextNode <= start or nextNode in visited:
                continue

            visited.add(nextNode)
            dfs(start, nextNode, first, visited, pathSum + nextNode, pathLength + 1)
            visited.remove(nextNode)

    for start in nodes:
        for first in neighbors[start]:
            if first <= start:
                continue
            visited = {start, first}
            dfs(start, first, first, visited, start + first, 2)

    return total


def sumPotencies(adjacency):
    if not adjacency:
        return 0

    pruneToTwoCore(adjacency)
    if not adjacency:
        return 0

    total = 0
    for componentEdges in biconnectedComponents(adjacency):
        vertices = set()
        blockAdjacency = {}

        for u, v in componentEdges:
            vertices.add(u)
            vertices.add(v)
            blockAdjacency.setdefault(u, set()).add(v)
            blockAdjacency.setdefault(v, set()).add(u)

        if len(vertices) < 3:
            continue

        if len(componentEdges) == len(vertices) and all(len(blockAdjacency[v]) == 2 for v in vertices):
            total += sum(vertices)
        else:
            total += cycleSumInBlock(blockAdjacency)

    return total


def FFromFullGraph(fullAdjacency, limit):
    return sumPotencies(inducedSubgraph(fullAdjacency, limit))


def solve(limit=10**6):
    return sumPotencies(buildGraph(limit))


def runTests(graph):
    assert FFromFullGraph(graph, 20) == 258
    assert FFromFullGraph(graph, 100) == 538_768


if __name__ == "__main__":
    fullGraph = buildGraph(10**6)
    runTests(fullGraph)
    start = time.time()
    answer = sumPotencies(fullGraph)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
