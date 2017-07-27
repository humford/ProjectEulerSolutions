import time
import math

#how many different way can a number be written
#as the sum of at least two positive integers
def count_sums(n):
    count = 0
    for i in range(n, 0, -1):
        for j in range(1, i+1):
            if i + j == n:
                count += count_sums(i) + count_sums(j)
    return count

start = time.time()
answer = count_sums(100)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
