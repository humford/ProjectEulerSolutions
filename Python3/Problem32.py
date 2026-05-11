def isPandigitalIdentity(multiplicand, multiplier, product):
    digits = "%s%s%s" % (multiplicand, multiplier, product)
    return len(digits) == 9 and set(digits) == set("123456789")


def pandigitalProducts():
    products = set()

    for multiplicand in range(2, 100):
        for multiplier in range(123, 10000 // multiplicand + 1):
            product = multiplicand * multiplier
            if isPandigitalIdentity(multiplicand, multiplier, product):
                products.add(product)

    return products


def runTests():
    assert isPandigitalIdentity(39, 186, 7254)


def solve():
    return sum(pandigitalProducts())


if __name__ == "__main__":
    runTests()
    print(solve())
