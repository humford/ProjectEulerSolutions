import math
import time

def ASieve(limit):
    is_prime = [False] * (limit + 1)

    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):

            n = 4 * x ** 2 + y ** 2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7:
                is_prime[n] = not is_prime[n]

            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11:
                is_prime[n] = not is_prime[n]

    for n in range(5, int(math.sqrt(limit))):
        if is_prime[n]:
            for k in range(n ** 2, limit + 1, n ** 2):
                is_prime[k] = False

    return is_prime

def totient_maximum(limit):
    is_prime = ASieve(int(math.sqrt(limit)))
    list_primes = [2, 3]

    for i in range(len(is_prime)):
        if is_prime[i]:
            list_primes.append(i)

    prime_product = 1
    for prime in list_primes:
        if prime_product*prime >= limit:
            break
        prime_product *= prime
    return prime_product

start = time.time()
answer = totient_maximum(1000000)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
