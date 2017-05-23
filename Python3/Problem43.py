import time
from itertools import permutations

def subStringDivisiblePandigital():
	test = permutations("0123456789")
	found = []
	divisors = [0, 2, 3, 5, 7, 11, 13, 17]
	for pandigital in test:
		divisible = True
		pd = "".join(pandigital)
		for digit in range(1, 8):
			sub = int(pd[digit:digit+3])
			if not sub % divisors[digit] == 0:
				divisible = False
				break
		if divisible:
			found.append(int(pd))
	return found


start = time.time()
answer = subStringDivisiblePandigital()
elapsed = (time.time() - start)

print("Found " + str(sum(answer)) + " in " + str(elapsed) + " seconds.")