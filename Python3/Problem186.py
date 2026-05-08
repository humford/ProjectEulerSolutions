import time


USER_COUNT = 1000000
PRIME_MINISTER = 524287


def laggedFibonacciGenerator():
    history = [0] * 55

    for k in range(1, 56):
        value = (100003 - 200003 * k + 300007 * k * k * k) % USER_COUNT
        history[k - 1] = value
        yield value

    index = 0
    while True:
        value = (history[(index + 31) % 55] + history[index]) % USER_COUNT
        history[index] = value
        index = (index + 1) % 55
        yield value


def find(parents, number):
    while parents[number] != number:
        parents[number] = parents[parents[number]]
        number = parents[number]
    return number


def union(parents, sizes, a, b):
    root_a = find(parents, a)
    root_b = find(parents, b)

    if root_a == root_b:
        return sizes[root_a]

    if sizes[root_a] < sizes[root_b]:
        root_a, root_b = root_b, root_a

    parents[root_b] = root_a
    sizes[root_a] += sizes[root_b]
    return sizes[root_a]


def successfulCallsForConnectedness(target_size):
    parents = list(range(USER_COUNT))
    sizes = [1] * USER_COUNT
    generator = laggedFibonacciGenerator()
    successful_calls = 0

    while sizes[find(parents, PRIME_MINISTER)] < target_size:
        caller = next(generator)
        called = next(generator)

        if caller == called:
            continue

        successful_calls += 1
        union(parents, sizes, caller, called)

    return successful_calls


def runTests():
    generator = laggedFibonacciGenerator()
    assert [next(generator) for _ in range(6)] == [
        200007,
        100053,
        600183,
        500439,
        600863,
        701497,
    ]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = successfulCallsForConnectedness(990000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
