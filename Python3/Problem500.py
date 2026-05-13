import heapq
import math
import time


MODULUS = 500_500_507


def _primes_at_least(count):
    if count < 6:
        limit = 15
    else:
        limit = int(count * (math.log(count) + math.log(math.log(count)))) + 100

    while True:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[:2] = b"\x00\x00"
        for p in range(2, int(limit ** 0.5) + 1):
            if sieve[p]:
                start = p * p
                sieve[start:limit + 1:p] = b"\x00" * (((limit - start) // p) + 1)
        primes = [value for value in range(limit + 1) if sieve[value]]
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def smallestWithDivisorPower(exponent_count, modulus=MODULUS):
    heap = _primes_at_least(exponent_count)
    heapq.heapify(heap)
    answer = 1
    for _ in range(exponent_count):
        value = heapq.heappop(heap)
        answer = answer * (value % modulus) % modulus
        heapq.heappush(heap, value * value)
    return answer


def runTests():
    assert smallestWithDivisorPower(4, 10 ** 9) == 120


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = smallestWithDivisorPower(500_500)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
