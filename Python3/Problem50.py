import math

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

def prime_sum(primes):
    sprimes = [0] * (len(primes))
    for x in range(1, len(primes)):
        sprimes[x] = sprimes[x - 1] + primes[x - 1]
    return sprimes

def consecutive_prime_sum(limit, primes):
    psum = prime_sum(primes)
    for x in range(1, len(psum)):
        if psum[x+1] > limit:
            return psum[x]

l = int(input("Largest Consecutive Prime Sum Below: "))
primes = ASieve(l)
primes = [2, 3] + [x for x in range(len(primes)) if primes[x]]
print(consecutive_prime_sum(l, primes))

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