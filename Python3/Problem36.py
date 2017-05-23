import time

def isPalindromic(n):
    n = list(str(n))
    for i, x in zip(n, reversed(n)):
        if i != x:
            return False
    else:
        return True

def doubleBasePalindromes(limit):
	palindromes = []
	for n in range(0, limit):
		if isPalindromic(n) and isPalindromic(int(bin(n)[2:])):
			palindromes.append(n)
	return palindromes

start = time.time()
answer = doubleBasePalindromes(1000000)
elapsed = (time.time() - start)

print("Found " + str(sum(answer)) + " in " + str(elapsed) + " seconds.")