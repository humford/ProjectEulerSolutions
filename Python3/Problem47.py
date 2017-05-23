import time

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return list(set(factors))

def fourIntWithNPrimeFactors(N):
	found = False
	n = 1
	while not found:
		if len(prime_factors(n)) >= N:
			group = [i for i in range(n, n+4)]
			nextInts = []
			for i in range(n+1, n+4):
				nextInts.append(len(prime_factors(i)))
			if nextInts[0] >= N and nextInts[1] >= N and nextInts[2] >= N:
				found = True
		n += 1
	return group

start = time.time()
answer = fourIntWithNPrimeFactors(4)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")