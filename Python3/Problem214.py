import time
from array import array


def totientChainPrimeSum(limit, target_length):
    phi = array("I", [0]) * limit
    chain_length = array("B", [0]) * limit
    primes = []
    phi[1] = 1
    chain_length[1] = 1
    total = 0

    for number in range(2, limit):
        is_prime = phi[number] == 0
        if is_prime:
            phi[number] = number - 1
            primes.append(number)

        chain_length[number] = chain_length[phi[number]] + 1
        if is_prime and chain_length[number] == target_length:
            total += number

        for prime in primes:
            multiple = number * prime
            if multiple >= limit:
                break

            if number % prime == 0:
                phi[multiple] = phi[number] * prime
                break

            phi[multiple] = phi[number] * (prime - 1)

    return total


def runTests():
    assert totientChainPrimeSum(10, 4) == 12


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = totientChainPrimeSum(40000000, 25)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
