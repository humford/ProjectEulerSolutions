import time
import math

#b = (p^2 - 2pa) / (2p - 2a)
#b is an integer for all solutions
def numSolutionsRightTriangle(p):
	solutions = 0
	for a in range(1, int(p/3)):
		if p * (p - 2 * a) % (2 * (p - a)) == 0:
			solutions += 1
	return solutions

def maxSolutionsPerimeter():
	pMax = 0
	maxSolutions = 0
	for p in range(2, 1000, 2):
		if numSolutionsRightTriangle(p) > maxSolutions:
			maxSolutions = numSolutionsRightTriangle(p)
			pMax = p
	return pMax

start = time.time()
answer = maxSolutionsPerimeter()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")