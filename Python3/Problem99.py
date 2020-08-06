import time
import math
import numpy as np

nums = open("../Files/p099_base_exp.txt", "r")
nums = nums.read()
numlist = nums.split("\n")

def compute_value(base_exp):
	l = base_exp.split(",")
	base = int(l[0])
	exp = int(l[1])

	return np.log(base) * exp

def compare_exponentials(numlist):
    i = 1
    highest = 0
    highest_line = 0

    for base_exp in numlist:
    	val = compute_value(base_exp)
    	if highest < val:
    		highest = val
    		highest_line = i
    	i += 1

    return highest_line


start = time.time()
answer = compare_exponentials(numlist)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
