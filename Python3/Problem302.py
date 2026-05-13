import bisect
import math
import time


LIMIT = 10**18


def integerCubeRoot(number):
    low = 0
    high = 1

    while high * high * high <= number:
        high *= 2

    while low + 1 < high:
        middle = (low + high) // 2

        if middle * middle * middle <= number:
            low = middle
        else:
            high = middle

    return low


def smallestPrimeFactorSieve(limit):
    smallest = [0] * (limit + 1)
    primes = []

    for number in range(2, limit + 1):
        if smallest[number] == 0:
            smallest[number] = number
            primes.append(number)

        for prime in primes:
            value = number * prime
            if value > limit or prime > smallest[number]:
                break
            smallest[value] = prime

    return primes, smallest


def factorWithSieve(number, smallest):
    factors = []

    while number > 1:
        prime = smallest[number]
        power = 0

        while number % prime == 0:
            number //= prime
            power += 1

        factors.append((prime, power))

    return factors


def countStrongAchilles(upper_exclusive):
    limit = upper_exclusive - 1
    max_prime = integerCubeRoot(limit // 4)

    if max_prime < 3:
        return 0

    primes, smallest = smallestPrimeFactorSieve(max_prime)
    previous_prime_factors = [
        factorWithSieve(prime - 1, smallest) if prime > 2 else []
        for prime in primes
    ]

    def phiGcdIsOne(phi_factors):
        gcd_value = 0

        for power in phi_factors.values():
            gcd_value = math.gcd(gcd_value, power)
            if gcd_value == 1:
                return True

        return False

    def applyPrime(index, prime, exponent, phi_factors, exponent_one):
        changes = []

        def addFactor(factor, power):
            existed = factor in phi_factors
            old_power = phi_factors[factor] if existed else 0
            changes.append((factor, old_power, existed))

            new_power = old_power + power
            phi_factors[factor] = new_power

            if old_power == 1:
                exponent_one.discard(factor)
            if new_power == 1:
                exponent_one.add(factor)

        addFactor(prime, exponent - 1)

        for factor, power in previous_prime_factors[index]:
            addFactor(factor, power)

        return changes

    def undo(changes, phi_factors, exponent_one):
        for factor, old_power, existed in reversed(changes):
            if existed:
                phi_factors[factor] = old_power
            else:
                del phi_factors[factor]

            if old_power == 1:
                exponent_one.add(factor)
            else:
                exponent_one.discard(factor)

    def search(max_index, number, exponent_gcd, phi_factors, exponent_one, prime_count):
        if prime_count == 1 and number * 4 > limit:
            return 0

        if exponent_one:
            lower_prime = max(exponent_one)
            if number * lower_prime * lower_prime > limit:
                return 0
        else:
            lower_prime = 2

        total = 0

        if (
            not exponent_one
            and prime_count >= 2
            and exponent_gcd == 1
            and phiGcdIsOne(phi_factors)
        ):
            total += 1

        if max_index < 0:
            return total

        remaining = limit // number
        if remaining < 4:
            return total

        upper_prime = min(primes[max_index], math.isqrt(remaining))
        if upper_prime < lower_prime:
            return total

        upper_index = min(max_index, bisect.bisect_right(primes, upper_prime) - 1)
        lower_index = bisect.bisect_left(primes, lower_prime)

        if lower_index > upper_index:
            return total

        for index in range(upper_index, lower_index - 1, -1):
            prime = primes[index]
            exponent = 2 if prime in phi_factors else 3
            prime_power = prime**exponent

            while prime_power <= remaining:
                changes = applyPrime(
                    index, prime, exponent, phi_factors, exponent_one
                )
                total += search(
                    index - 1,
                    number * prime_power,
                    math.gcd(exponent_gcd, exponent),
                    phi_factors,
                    exponent_one,
                    prime_count + 1,
                )
                undo(changes, phi_factors, exponent_one)

                exponent += 1
                prime_power *= prime

        return total

    total = 0

    for index in range(len(primes) - 1, 0, -1):
        prime = primes[index]
        exponent = 3
        prime_power = prime**exponent

        while prime_power * 4 <= limit:
            phi_factors = {prime: exponent - 1}
            exponent_one = set()

            for factor, power in previous_prime_factors[index]:
                new_power = phi_factors.get(factor, 0) + power
                phi_factors[factor] = new_power
                if new_power == 1:
                    exponent_one.add(factor)
                else:
                    exponent_one.discard(factor)

            total += search(index - 1, prime_power, exponent, phi_factors, exponent_one, 1)

            exponent += 1
            prime_power *= prime

    return total


def runTests():
    assert countStrongAchilles(10**4) == 7
    assert countStrongAchilles(10**8) == 656


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = countStrongAchilles(LIMIT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
