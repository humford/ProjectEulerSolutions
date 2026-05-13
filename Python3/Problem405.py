import time


MODULUS = 17**7
EXPONENT_PERIOD = 16 * 17**6


def tilingPointCount(index, modulus=None):
    sign = 1 if index % 2 == 1 else -1
    if modulus is None:
        numerator = sign - 5 * 2 ** (index + 2) + 6 * 4**index
        return numerator // 15 + 1

    inverse15 = pow(15, -1, modulus)
    numerator = (
        sign
        - 5 * pow(2, index + 2, modulus)
        + 6 * pow(4, index, modulus)
    )
    return (numerator * inverse15 + 1) % modulus


def hugeTilingPointCount(power=10**18, modulus=MODULUS):
    indexModPeriod = pow(10, power, EXPONENT_PERIOD)
    inverse15 = pow(15, -1, modulus)
    numerator = (
        -1
        - 5 * pow(2, indexModPeriod + 2, modulus)
        + 6 * pow(4, indexModPeriod, modulus)
    )
    return (numerator * inverse15 + 1) % modulus


def runTests():
    assert tilingPointCount(1) == 0
    assert tilingPointCount(4) == 82
    assert tilingPointCount(10**9, MODULUS) == 126897180


if __name__ == "__main__":
    start = time.time()
    runTests()
    print("Found", hugeTilingPointCount(), "in", time.time() - start, "seconds.")
