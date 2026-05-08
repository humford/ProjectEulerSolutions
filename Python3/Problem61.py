import time


def polygonalNumber(kind, n):
    if kind == 3:
        return n * (n + 1) // 2
    if kind == 4:
        return n * n
    if kind == 5:
        return n * (3 * n - 1) // 2
    if kind == 6:
        return n * (2 * n - 1)
    if kind == 7:
        return n * (5 * n - 3) // 2
    if kind == 8:
        return n * (3 * n - 2)
    raise ValueError("Unknown polygonal kind " + str(kind))


def fourDigitPolygonals():
    values = {}

    for kind in range(3, 9):
        values[kind] = []
        n = 1
        while True:
            value = polygonalNumber(kind, n)
            if value >= 10000:
                break
            if value >= 1000 and value % 100 >= 10:
                values[kind].append(value)
            n += 1

    return values


def findCyclicFigurateSet():
    values_by_kind = fourDigitPolygonals()

    def search(chain, remaining_kinds):
        if not remaining_kinds:
            if chain[-1] % 100 == chain[0] // 100:
                return chain
            return None

        suffix = chain[-1] % 100
        for kind in remaining_kinds:
            for value in values_by_kind[kind]:
                if value // 100 != suffix:
                    continue

                result = search(chain + [value], remaining_kinds - {kind})
                if result is not None:
                    return result

        return None

    for start in values_by_kind[8]:
        result = search([start], set(range(3, 8)))
        if result is not None:
            return result

    raise ValueError("No cyclic figurate set found")


def runTests():
    assert polygonalNumber(3, 1) == 1
    assert polygonalNumber(4, 10) == 100
    assert polygonalNumber(8, 19) == 1045


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer_set = findCyclicFigurateSet()
    answer = sum(answer_set)
    elapsed = time.time() - start

    print("Set " + str(answer_set))
    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
