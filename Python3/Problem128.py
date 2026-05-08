import time


def isPrime(n):
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in (2, 3, 5, 7, 11):
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def firstTile(layer):
    return 3 * layer * (layer - 1) + 2


def lastTile(layer):
    return 3 * layer * (layer + 1) + 1


def firstTileHasPD3(layer):
    return isPrime(6 * layer - 1) and isPrime(6 * layer + 1) and isPrime(12 * layer + 5)


def lastTileHasPD3(layer):
    return (
        layer > 1
        and isPrime(6 * layer - 1)
        and isPrime(6 * layer + 5)
        and isPrime(12 * layer - 7)
    )


def pd3Tiles(count):
    values = [1]
    layer = 1

    while len(values) < count:
        if firstTileHasPD3(layer):
            values.append(firstTile(layer))
        if len(values) == count:
            break
        if lastTileHasPD3(layer):
            values.append(lastTile(layer))
        layer += 1

    return values


def runTests():
    assert pd3Tiles(6) == [1, 2, 8, 19, 20, 37]


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pd3Tiles(2000)[-1]
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
