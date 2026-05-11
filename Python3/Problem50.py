def primeSieve(limit):
    is_prime = [True] * limit
    if limit > 0:
        is_prime[0] = False
    if limit > 1:
        is_prime[1] = False

    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit, value):
                is_prime[multiple] = False

    return is_prime


def consecutivePrimeSum(limit):
    primes = [value for value, is_prime in enumerate(primeSieve(limit)) if is_prime]
    prime_set = set(primes)
    prefix = [0]

    for prime in primes:
        prefix.append(prefix[-1] + prime)

    best_sum = 0
    best_length = 0

    for start in range(len(prefix)):
        for end in range(start + best_length + 1, len(prefix)):
            total = prefix[end] - prefix[start]
            if total >= limit:
                break
            if total in prime_set:
                best_sum = total
                best_length = end - start

    return best_sum


def runTests():
    assert consecutivePrimeSum(100) == 41
    assert consecutivePrimeSum(1000) == 953


def solve():
    return consecutivePrimeSum(1000000)


if __name__ == "__main__":
    runTests()
    print(solve())
