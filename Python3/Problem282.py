import time


MODULUS = 14**8
STABLE_TOWER_HEIGHT = 200
SMALL_TOWERS = {1: 2, 2: 4, 3: 16, 4: 65536}


def factorization(number):
    factors = {}
    divisor = 2

    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            number //= divisor

        divisor += 1 if divisor == 2 else 2

    if number > 1:
        factors[number] = factors.get(number, 0) + 1

    return factors


def factorizationValue(factors):
    result = 1

    for prime, power in factors.items():
        result *= prime**power

    return result


def carmichael(factors):
    result_factors = {}

    for prime, power in factors.items():
        if prime == 2 and power >= 3:
            component = {2: power - 2}
        else:
            component = factorization(prime - 1)
            if power > 1:
                component[prime] = max(component.get(prime, 0), power - 1)

        for component_prime, component_power in component.items():
            if component_power > result_factors.get(component_prime, 0):
                result_factors[component_prime] = component_power

    return factorizationValue(result_factors), result_factors


def powerTowerMod(height, modulus, factors=None, minimum=0):
    if modulus == 1:
        return minimum

    if height <= 4:
        exact_value = SMALL_TOWERS[height]
        result = exact_value % modulus

        while exact_value >= minimum and result < minimum:
            result += modulus

        return result

    if factors is None:
        factors = factorization(modulus)

    reduced_modulus, reduced_factors = carmichael(factors)
    exponent = powerTowerMod(
        height - 1,
        reduced_modulus,
        reduced_factors,
        max(factors.values()) if factors else 0,
    )
    result = pow(2, exponent, modulus)

    while result < minimum:
        result += modulus

    return result


def smallAckermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return smallAckermann(m - 1, 1)

    return smallAckermann(m - 1, smallAckermann(m, n - 1))


def ackermannDiagonalSumMod(modulus):
    total = sum(smallAckermann(n, n) for n in range(4))
    total += powerTowerMod(7, modulus) - 3

    stable_tower = powerTowerMod(STABLE_TOWER_HEIGHT, modulus)
    total += 2 * (stable_tower - 3)

    return total % modulus


def runTests():
    assert smallAckermann(1, 0) == 2
    assert smallAckermann(2, 2) == 7
    assert smallAckermann(3, 4) == 125
    assert powerTowerMod(3, 1000) == 16


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = ackermannDiagonalSumMod(MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
