import time
import math

def squarerootconvergents(limit):
    result = 0
    den = 2
    num = 3
    for i in range(1, limit+1):
        num += 2 * den
        den = num - den
        if int(math.log10(num)) > int(math.log10(den)):
            result += 1
    return result

start = time.time()
answer = squarerootconvergents(1000)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
