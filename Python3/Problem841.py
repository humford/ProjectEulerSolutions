import math
import time


def kahanSum(values):
    total = 0.0
    correction = 0.0

    for value in values:
        adjusted = value - correction
        nextTotal = total + adjusted
        correction = (nextTotal - total) - adjusted
        total = nextTotal

    return total


def A(p, q):
    if p <= 2 * q or q <= 0 or math.gcd(p, q) != 1:
        raise ValueError("expected coprime integers p > 2q > 0")

    angle = math.pi / p
    scaledSine = p * math.sin(angle)
    oddSign = 1.0 if q % 2 else -1.0
    previousCosine = 1.0
    terms = []

    for k in range(1, q + 1):
        currentCosine = math.cos(k * angle)
        sign = oddSign if k % 2 else -oddSign
        terms.append(sign / (currentCosine * previousCosine))
        previousCosine = currentCosine

    return scaledSine * kahanSum(terms)


def fibonacciNumbers(n):
    values = [0, 1]
    for _ in range(2, n + 1):
        values.append(values[-1] + values[-2])
    return values


def solve():
    fibonacci = fibonacciNumbers(35)
    return format(
        kahanSum(A(fibonacci[n + 1], fibonacci[n - 1]) for n in range(3, 35)),
        ".10f",
    )


def runTests():
    assert format(A(8, 3), ".10f") == "9.9411254970"
    assert format(A(130021, 50008), ".10f") == "10.9210371479"


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = solve()
    elapsed = time.time() - start

    print("Found " + answer + " in " + str(elapsed) + " seconds.")
