import time
import math
from itertools import permutations

def arePermutations(a, b):
    return sorted([d for d in str(a)]) == sorted([d for d in str(b)])

def isCube(n):
    r = int(round(n ** (1. / 3)))
    return r ** 3 == n

def smallestCubicPermutation(perms):
    r = 0
    cube_perms = {}
    smallest_perms = {}
    while 1:
        r += 1
        r_cube = r ** 3
        index = tuple(sorted([int(l) for l in str(r_cube)]))
        if index not in cube_perms.keys():
            cube_perms[index] = 1
            smallest_perms[index] = r_cube
        else:
            cube_perms[index] += 1
            if cube_perms[index] == perms:
                return smallest_perms[index]

start = time.time()
answer = smallestCubicPermutation(5)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
