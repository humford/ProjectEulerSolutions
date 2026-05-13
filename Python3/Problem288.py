import time


P = 61
Q = 10**7
POWER = 10
RANDOM_MODULUS = 50515093
SEED = 290797


def pFactorialFactorCount(prime, limit, power):
    modulus = prime**power
    random_state = SEED
    coefficient = 0
    prime_power = 1
    total = 0

    for _ in range(limit + 1):
        total = (total + (random_state % prime) * coefficient) % modulus
        coefficient = (coefficient + prime_power) % modulus
        prime_power = (prime_power * prime) % modulus
        random_state = (random_state * random_state) % RANDOM_MODULUS

    return total


def runTests():
    assert pFactorialFactorCount(3, 10000, 20) == 624955285


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = pFactorialFactorCount(P, Q, POWER)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
