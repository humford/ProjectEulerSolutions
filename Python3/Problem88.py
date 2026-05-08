import time


def minimalProductSums(limit):
    maximum_product = 2 * limit
    minimal = [maximum_product] * (limit + 1)

    def search(product, total, factor_count, start):
        k = product - total + factor_count
        if k <= limit:
            minimal[k] = min(minimal[k], product)

        factor = start
        while product * factor <= maximum_product:
            search(product * factor, total + factor, factor_count + 1, factor)
            factor += 1

    search(1, 0, 0, 2)
    return minimal


def sumMinimalProductSums(limit):
    return sum(set(minimalProductSums(limit)[2:]))


def runTests():
    assert sumMinimalProductSums(12) == 61


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = sumMinimalProductSums(12000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
