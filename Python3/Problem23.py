#non-ideal solution
from sympy.ntheory import divisor_sigma
from time import time

start = time()

def sumDivisors(n):
	sumdivisors = 0
	for x in range(1, int((n/2)+1)):
		if n % x == 0:
			sumdivisors += x
	return sumdivisors

abundant = []
for i in range(2, 28123 + 1):
	if divisor_sigma(i, 1) > 2*i:
		abundant.append(i)

canBeWrittenAsAbundant = {}
for i in range(1, 28123 + 1):
	canBeWrittenAsAbundant[i] = False

for i in range(len(abundant)):
	for j in range(i, len(abundant)):
		if abundant[i] + abundant[j] <= 28123:
			canBeWrittenAsAbundant[abundant[i] + abundant[j]] = True
		else:
			break

total = 0
for i in range(1, 28123 + 1):
	if not canBeWrittenAsAbundant[i]:
		total += i

print(total, time() - start)