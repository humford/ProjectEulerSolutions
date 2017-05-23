import time
from itertools import permutations
from fractions import gcd

# bad idea:
# def digitCancellingFractions():
# 	test_numerator = [x for x in range(10, 100)]
# 	test_denominator = [x for x in range(10, 100)]
# 	for n in test_numerator:
# 		for d in test_denominator:
# 			overlaps = [int(x) for x in list(set(str(n)) & set(str(d)))]
# 			if 0 in overlaps:
# 				overlaps = overlaps.remove(0)
# 			if overlaps and len(overlaps) > 1:
# 				f = (n / d).as_integer_ratio()
# 				if f[0] in [2,3,4,5,6,7,8,9] and f[1] in [2,3,4,5,6,7,8,9]:
# 					print(n, d, overlaps, f)
# 	return 0

def digitCancellingFractions():
	denproduct = 1
	nomproduct = 1
	for i in range(1, 10):
		for den in range(1, i):
			for nom in range(1, den):
				if (nom * 10 + i) * den == nom * (i * 10 + den):
					denproduct *= den
					nomproduct *= nom
	denproduct /= gcd(nomproduct, denproduct)
	return int(denproduct)

start = time.time()
answer = digitCancellingFractions()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")