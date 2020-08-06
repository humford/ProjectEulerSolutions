import math
import time
import itertools

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

def semiprimes(limit):
    is_prime = ASieve(limit)
    list_primes = [2, 3]

    for i in range(len(is_prime)):
        if is_prime[i]:
            list_primes.append(i)

    list_semiprimes = []
    pairs = list(itertools.combinations(list_primes, 2))
    for prime in list_primes:
        c = prime ** 2
        if c < limit:
            list_semiprimes.append(c)
    for pair in pairs:
        c = pair[0] * pair[1]
        if c < limit:
            list_semiprimes.append(c)

    #print(list_semiprimes)
    return len(list_semiprimes)

# How many composite integers, n < 10^8, have precisely two, not necessarily distinct, prime factors?

start = time.time()
answer = semiprimes(10 ** 8)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
