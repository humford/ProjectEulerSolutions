#non-ideal solution
from itertools import combinations

def sumDivisors(n):
	sumdivisors = 0
	for x in range(1, int((n/2)+1)):
		if n % x == 0:
			sumdivisors += x
	return sumdivisors

abundant = []
for i in range(2, 28123 + 1):
	if sumDivisors(i) > i:
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

print(total)