import time
import collections

numerals = open("../Files/p089_roman.txt", "r")
numerals = numerals.read()
numeral_list = numerals.split("\n")

numeral_values = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}

# I = 1
# V = 5
# X = 10
# L = 50
# C = 100
# D = 500
# M = 1000

# Numerals must be arranged in descending order of size.
# M, C, and X cannot be equalled or exceeded by smaller denominations.
# D, L, and V can each only appear once.

#print(numeral_list)

def minimize_numeral(numeral):
	num = 0
	l_num = [char for char in numeral]
	cnt = collections.Counter(l_num)
	print(cnt)

	for k in cnt:
		num += numeral_values[k] * cnt[k]

	print(num)

def count_extra_characters(numeral_list):
	for numeral in numeral_list:
		minimize_numeral(numeral)
	return 0

start = time.time()
answer = count_extra_characters(numeral_list)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")