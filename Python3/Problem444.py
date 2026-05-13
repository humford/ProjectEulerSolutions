import hashlib
import math
import time


TARGET_MD5 = "e6745c386ba3c0de1bf56897e453c7c8"


def harmonic(number):
    return sum(1 / value for value in range(1, number + 1))


def repeatedLotterySumLog10(iterations, limit):
    top = limit + iterations
    logCombination = (
        math.lgamma(top + 1) / math.log(10)
        - math.lgamma(limit + 1) / math.log(10)
        - math.lgamma(iterations + 1) / math.log(10)
    )

    if top < 10**6:
        harmonicDifference = harmonic(top) - harmonic(iterations)
    else:
        gamma = 0.5772156649015328606
        harmonicTop = math.log(top) + gamma + 1 / (2 * top) - 1 / (12 * top * top)
        harmonicDifference = harmonicTop - harmonic(iterations)

    return logCombination + math.log10(harmonicDifference)


def scientificAnswer(iterations, limit):
    logValue = repeatedLotterySumLog10(iterations, limit)
    exponent = math.floor(logValue)
    mantissa = 10 ** (logValue - exponent)
    answer = f"{mantissa:.9f}e{exponent}"

    if answer.startswith("10."):
        exponent += 1
        answer = f"{mantissa / 10:.9f}e{exponent}"

    return answer


def runTests():
    assert format(harmonic(111), ".4f") == "5.2912"
    assert scientificAnswer(3, 100) == "5.983679014e5"
    assert hashlib.md5(scientificAnswer(20, 10**14).encode()).hexdigest() == TARGET_MD5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = scientificAnswer(20, 10**14)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
