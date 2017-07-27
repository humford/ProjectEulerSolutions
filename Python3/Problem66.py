import time
import math
import sys
from scipy.optimize import minimize

# x = math.sqrt(1.0 + D * y ** 2.0)

def Dio_solution(y, D):
    x = math.sqrt(1.0 + float(D) * float(y) ** 2.0)
    if float(x).is_integer():
        return int(x)
    return -1

def find_min_Dio(D):
    s = -1
    y = 0
    while s == -1:
        y += 1
        s = Dio_solution(y, D)
        print(y, D, s)
    return s

def find_min_Dio_fast(D):
    pass

def find_largest_min_Dio(limit):
    largest = 0
    for D in range(2, limit+1):
        if not float(math.sqrt(D)).is_integer():
            x = find_min_Dio(D)
            if x > largest:
                largest = x
    return largest

start = time.time()
answer = find_largest_min_Dio(100)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
