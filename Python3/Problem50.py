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

def sum_primes(n, primes):
    return sum(primes[:n-1])

def generate_prime_sums(primes):
    prime_sums = [0 for p in range(len(primes))]
    for i in range(len(primes)-1):
        prime_sums[i+1] = prime_sums[i] + primes[i]
    return prime_sums

def consecutive_prime_sum(limit, prime_sums):
    largest_pindex = 0
    largest_psum = 0
    for j in range(len(primes)):
        if j < largest_pindex:
            break
        for k in range(j-1-largest_pindex, -1,-1):
            i = j-k
            s = prime_sums[j] - prime_sums[k]
            if s > limit:
                break
            if s in primes and i > largest_pindex:
                largest_pindex = i
                largest_psum = s
    return largest_psum

l = int(input("Largest Consecutive Prime Sum Below: "))
primes = ASieve(l)
primes = [2, 3] + [x for x in range(len(primes)) if primes[x]]

start = time.time()
answer = consecutive_prime_sum(l, generate_prime_sums(primes))
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

# const
# int
# limit = 1000000;
# long
# result = 0;
# int
# numberOfPrimes = 0;
# long[]
# primes = ESieve(1, limit);
# long[]
# primeSum = new
# long[primes.Length + 1];
#
# primeSum[0] = 0;
# for (int i = 0; i < primes.Length; i++) {
# primeSum[i+1] = primeSum[i] + primes[i];
# }
#
# for (int i = numberOfPrimes; i < primeSum.Length; i++) {
# for (int j = i-(numberOfPrimes+1); j >= 0; j--) {
# if (primeSum[i] - primeSum[j] > limit)
# break;
#
# if (Array.BinarySearch(primes, primeSum[i] - primeSum[j]) >= 0) {
# numberOfPrimes = i - j;
# result = primeSum[i] - primeSum[j];
# }
# }
# }