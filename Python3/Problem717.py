import time


def primeSieve(limit):
    if limit < 2:
        return bytearray(limit + 1)

    isPrime = bytearray(b"\x01") * limit
    isPrime[0] = 0
    isPrime[1] = 0

    for n in range(4, limit, 2):
        isPrime[n] = 0

    candidate = 3
    while candidate * candidate < limit:
        if isPrime[candidate]:
            start = candidate * candidate
            step = 2 * candidate
            isPrime[start:limit:step] = b"\x00" * (((limit - 1 - start) // step) + 1)
        candidate += 2

    return isPrime


def modularFormula(prime):
    if prime == 3:
        return 5

    exponent = pow(2, prime, prime - 1)
    residue = pow(2, exponent, prime)
    halfResidue = residue * ((prime + 1) // 2) % prime
    lifted = halfResidue * pow(2, prime, prime * prime) % (prime * prime)
    return ((lifted - residue) % (prime * prime)) // prime


def reducedFormula(prime):
    return modularFormula(prime) % prime


def modularFormulaPrimeSum(limit):
    isPrime = primeSieve(limit)
    total = 0

    for prime in range(3, limit, 2):
        if isPrime[prime]:
            total += reducedFormula(prime)

    return total


def runTests():
    assert modularFormula(3) == 5
    assert reducedFormula(31) == 17
    assert modularFormulaPrimeSum(100) == 474
    assert modularFormulaPrimeSum(10 ** 4) == 2_819_236


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = modularFormulaPrimeSum(10 ** 7)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
