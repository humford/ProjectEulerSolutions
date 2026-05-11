def nonMersennePrimeLastDigits(coefficient, exponent, addend, digits):
    modulus = 10 ** digits
    return (coefficient * pow(2, exponent, modulus) + addend) % modulus


def runTests():
    assert nonMersennePrimeLastDigits(1, 10, 0, 5) == 1024


def solve():
    return nonMersennePrimeLastDigits(28433, 7830457, 1, 10)


if __name__ == "__main__":
    runTests()
    print(str(solve()).zfill(10))
