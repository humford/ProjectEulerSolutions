from array import array
import time


MODULUS = 10**18
LIMIT = 60000000


def divisorCounts(limit):
    smallestPrime = array("I", [0]) * (limit + 1)
    primeExponent = array("B", [0]) * (limit + 1)
    counts = array("H", [0]) * (limit + 1)
    primes = array("I")
    counts[1] = 1

    for number in range(2, limit + 1):
        if smallestPrime[number] == 0:
            smallestPrime[number] = number
            primeExponent[number] = 1
            counts[number] = 2
            primes.append(number)

        numberSmallestPrime = smallestPrime[number]
        numberExponent = primeExponent[number]
        numberCount = counts[number]

        for prime in primes:
            product = number * prime

            if product > limit:
                break

            smallestPrime[product] = prime

            if prime == numberSmallestPrime:
                exponent = numberExponent + 1
                primeExponent[product] = exponent
                counts[product] = numberCount // (numberExponent + 1) * (exponent + 1)
                break

            primeExponent[product] = 1
            counts[product] = numberCount * 2

    return counts


def addToFenwick(tree, index, value):
    while index < len(tree):
        tree[index] += value
        index += index & -index


def fenwickPrefixSum(tree, index):
    total = 0

    while index > 0:
        total += tree[index]
        index -= index & -index

    return total


def triangleTriples(limit=LIMIT, modulus=MODULUS):
    divisors = divisorCounts(limit + 1)
    frequencies = [0, 0]

    for number in range(1, limit + 1):
        if number % 2 == 0:
            value = divisors[number // 2] * divisors[number + 1]
        else:
            value = divisors[number] * divisors[(number + 1) // 2]

        if value >= len(frequencies):
            frequencies.extend([0] * (value + 1 - len(frequencies)))

        frequencies[value] += 1

    leftTree = [0] * len(frequencies)
    rightTree = [0] * len(frequencies)

    for value, count in enumerate(frequencies):
        if count > 0:
            addToFenwick(rightTree, value, count)

    leftCount = 0
    total = 0

    for number in range(1, limit + 1):
        if number % 2 == 0:
            value = divisors[number // 2] * divisors[number + 1]
        else:
            value = divisors[number] * divisors[(number + 1) // 2]

        addToFenwick(rightTree, value, -1)
        leftGreater = leftCount - fenwickPrefixSum(leftTree, value)
        rightLess = fenwickPrefixSum(rightTree, value - 1)
        total = (total + leftGreater * rightLess) % modulus

        addToFenwick(leftTree, value, 1)
        leftCount += 1

    return total


def runTests():
    assert triangleTriples(20) == 14
    assert triangleTriples(100) == 5772
    assert triangleTriples(1000) == 11174776


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = triangleTriples()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
