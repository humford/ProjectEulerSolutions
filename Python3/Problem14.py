def collatzLength(n, cache):
    original = n
    seen = []

    while n not in cache:
        seen.append(n)
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

    length = cache[n]
    for value in reversed(seen):
        length += 1
        cache[value] = length

    return cache[original]


def longestCollatzStartBelow(limit):
    cache = {1: 1}
    best_start = 1
    best_length = 1

    for start in range(2, limit):
        length = collatzLength(start, cache)
        if length > best_length:
            best_start = start
            best_length = length

    return best_start


def runTests():
    cache = {1: 1}
    assert collatzLength(13, cache) == 10


def solve():
    return longestCollatzStartBelow(1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
