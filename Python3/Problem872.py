import time


def parentInTree(n, k):
    if k == n:
        return 0
    return k + (1 << ((n - k).bit_length() - 1))


def f(n, k):
    total = 0

    while k:
        total += k
        k = parentInTree(n, k)

    return total


def buildParents(limit):
    parent = {1: 0}
    children = {1: []}
    root = 1

    for n in range(2, limit + 1):
        path = []
        node = root
        while True:
            path.append(node)
            if not children[node]:
                break
            node = max(children[node])

        for node in path:
            oldParent = parent[node]
            if oldParent:
                children[oldParent].remove(node)
            parent[node] = n

        children[n] = path[:]
        parent[n] = 0
        root = n

    return parent


def bruteF(n, k):
    parent = buildParents(n)
    total = 0

    while k:
        total += k
        k = parent[k]

    return total


def runTests():
    assert f(6, 1) == 12
    assert f(10, 3) == 29
    for n in range(1, 25):
        for k in range(1, n + 1):
            assert f(n, k) == bruteF(n, k)


def solve():
    return f(10**17, 9**17)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
