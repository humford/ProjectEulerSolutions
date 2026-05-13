import time


BOWL_COUNT = 1500


def beanCounts(count):
    value = 123456
    beans = []

    for _ in range(count):
        if value % 2 == 0:
            value //= 2
        else:
            value = (value // 2) ^ 926252

        beans.append(value % (2**11) + 1)

    return beans


def minimalFinalSecondMoment(totalBeans, firstMoment):
    baseSum = totalBeans * (totalBeans - 1) // 2
    shift, extra = divmod(firstMoment - baseSum, totalBeans)
    sumIndices = totalBeans * (totalBeans - 1) // 2
    sumSquares = totalBeans * (totalBeans - 1) * (2 * totalBeans - 1) // 6

    total = (
        totalBeans * shift * shift
        + 2 * shift * sumIndices
        + sumSquares
    )

    if extra > 0:
        first = totalBeans - extra
        last = totalBeans - 1
        movedIndexSum = (first + last) * extra // 2
        total += 2 * (extra * shift + movedIndexSum) + extra

    return total


def spillingMoves(beans):
    totalBeans = sum(beans)
    firstMoment = sum(index * count for index, count in enumerate(beans))
    initialSecondMoment = sum(index * index * count for index, count in enumerate(beans))
    finalSecondMoment = minimalFinalSecondMoment(totalBeans, firstMoment)

    return (finalSecondMoment - initialSecondMoment) // 2


def answer():
    return spillingMoves(beanCounts(BOWL_COUNT))


def runTests():
    assert beanCounts(2) == [289, 145]
    assert spillingMoves(beanCounts(2)) == 3419100


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")
