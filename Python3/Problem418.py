import math
import time


def factorization(number):
    factors = []
    divisor = 2

    while divisor * divisor <= number:
        if number % divisor == 0:
            exponent = 0

            while number % divisor == 0:
                number //= divisor
                exponent += 1

            factors.append((divisor, exponent))

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors.append((number, 1))

    return factors


def numberFromFactors(factors):
    number = 1

    for prime, exponent in factors:
        number *= prime**exponent

    return number


def integerCubeRoot(number):
    low = 0
    high = 1

    while high**3 <= number:
        high *= 2

    while low + 1 < high:
        middle = (low + high) // 2

        if middle**3 <= number:
            low = middle
        else:
            high = middle

    return low


def divisorsFromFactors(factors):
    divisors = [1]

    for prime, exponent in factors:
        nextDivisors = []
        power = 1

        for _ in range(exponent + 1):
            for divisor in divisors:
                nextDivisors.append(divisor * power)

            power *= prime

        divisors = nextDivisors

    return sorted(divisors)


def divisorsInRange(factors, low, high):
    orderedFactors = sorted(factors)
    suffixProducts = [1] * (len(orderedFactors) + 1)

    for index in range(len(orderedFactors) - 1, -1, -1):
        prime, exponent = orderedFactors[index]
        suffixProducts[index] = suffixProducts[index + 1] * prime**exponent

    divisors = []

    def search(index, current):
        if current > high or current * suffixProducts[index] < low:
            return

        if index == len(orderedFactors):
            if low <= current <= high:
                divisors.append(current)

            return

        prime, exponent = orderedFactors[index]
        power = 1

        for _ in range(exponent + 1):
            search(index + 1, current * power)
            power *= prime

    search(0, 1)
    return sorted(divisors)


def bestFactorTripleSum(number):
    divisors = divisorsFromFactors(factorization(number))
    best = None

    for a in divisors:
        if a * a * a > number:
            break

        remainder = number // a

        for b in divisors:
            if b < a:
                continue
            if b * b > remainder:
                break
            if remainder % b:
                continue

            c = remainder // b

            if b <= c and (best is None or c * best[0] < best[2] * a):
                best = (a, b, c)

    return sum(best)


def bestFactorTripleInRange(number, factors, low, high):
    root = integerCubeRoot(number)
    divisors = divisorsInRange(factors, low, high)
    possibleSmallFactors = [divisor for divisor in divisors if divisor <= root]
    possibleLargeFactors = [divisor for divisor in divisors if divisor >= root]
    best = None

    for a in possibleSmallFactors:
        for c in possibleLargeFactors:
            if best is not None and c * best[0] >= best[2] * a:
                break

            product = a * c

            if number % product:
                continue

            b = number // product

            if a <= b <= c:
                best = (a, b, c)

    return best


def boundedFactorTripleSum(number, factors, partsPerMillion):
    root = integerCubeRoot(number)
    scale = 1_000_000
    low = root * (scale - partsPerMillion) // scale
    high = (root * (scale + partsPerMillion) + scale - 1) // scale
    best = bestFactorTripleInRange(number, factors, low, high)

    if best is None:
        raise ValueError("search window did not contain a factorisation triple")

    a, _, c = best

    # If another triple had a smaller c/a ratio, then its a and c would both
    # lie inside these cube-root bounds.  The chosen search window must cover
    # that whole improvement region before the candidate can be accepted.
    assert low**3 * c**2 <= number * a**2
    assert high**3 * a**2 >= number * c**2

    return sum(best)


def factorialFactorTripleSum(limit, partsPerMillion):
    number = math.factorial(limit)
    factors = factorization(number)

    return boundedFactorTripleSum(number, factors, partsPerMillion)


def runTests():
    assert bestFactorTripleSum(165) == 19
    assert bestFactorTripleSum(100100) == 142
    assert factorialFactorTripleSum(20, 4_000) == 4034872


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = factorialFactorTripleSum(43, 1_000)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
