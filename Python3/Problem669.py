import time


def fibonacciNumbersUpTo(limit):
    numbers = [1, 1]
    while numbers[-1] < limit:
        numbers.append(numbers[-1] + numbers[-2])
    return numbers


def isFibonacci(number):
    return fibonacciNumbersUpTo(number)[-1] == number


def previousFibonacci(number):
    numbers = fibonacciNumbersUpTo(number)
    if numbers[-1] != number:
        raise ValueError("number is not Fibonacci")
    return numbers[-2]


def knightAtRightChair(chairFromRight, knightCount):
    previous = previousFibonacci(knightCount)
    if chairFromRight == 1:
        return knightCount

    multiplier = chairFromRight // 2
    if chairFromRight % 2 == 0:
        return (previous * multiplier) % knightCount
    return (-previous * multiplier) % knightCount


def fibonacciSumGraph(knightCount):
    fibonacciSums = set(fibonacciNumbersUpTo(2 * knightCount))
    graph = {knight: [] for knight in range(1, knightCount + 1)}
    for knight in range(1, knightCount + 1):
        for total in fibonacciSums:
            neighbor = total - knight
            if 1 <= neighbor <= knightCount and neighbor != knight:
                graph[knight].append(neighbor)
        graph[knight].sort()
    return graph


def bruteArrangement(knightCount):
    graph = fibonacciSumGraph(knightCount)
    endpoints = sorted(
        knight
        for knight, neighbors in graph.items()
        if len(neighbors) == 1
    )
    starts = endpoints or range(1, knightCount + 1)

    for start in starts:
        used = {start}
        path = [start]

        def search(current):
            if len(path) == knightCount:
                return path[0] < path[-1]

            candidates = [
                neighbor
                for neighbor in graph[current]
                if neighbor not in used
            ]
            candidates.sort(
                key=lambda neighbor: sum(
                    1
                    for nextNeighbor in graph[neighbor]
                    if nextNeighbor not in used
                )
            )

            for neighbor in candidates:
                used.add(neighbor)
                path.append(neighbor)
                if search(neighbor):
                    return True
                path.pop()
                used.remove(neighbor)
            return False

        if search(start):
            return path

    raise ValueError("no seating arrangement found")


def knightAtChair(knightCount, chairFromLeft):
    if isFibonacci(knightCount):
        chairFromRight = knightCount - chairFromLeft + 1
        return knightAtRightChair(chairFromRight, knightCount)

    return bruteArrangement(knightCount)[chairFromLeft - 1]


def runTests():
    assert knightAtChair(7, 3) == 7
    assert knightAtChair(34, 3) == 30


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = knightAtChair(
        99_194_853_094_755_497,
        10_000_000_000_000_000,
    )
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
