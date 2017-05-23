import time
from itertools import permutations

def pandigitalProducts():
	test = permutations("123456789")
	pdproducts = []
	for pandigital in test:
		pd = "".join(pandigital)
		for d1 in range(1, 4):
			for d2 in range(d1+1, 6):
				multiplicand = int(pd[:d1])
				multiplier = int(pd[d1:d2])
				product = int(pd[d2:])
				if multiplicand * multiplier == product:
					pdproducts.append(product)
	return list(set(pdproducts))

start = time.time()
answer = pandigitalProducts()
elapsed = (time.time() - start)

print("Found " + str(sum(answer)) + " in " + str(elapsed) + " seconds.")