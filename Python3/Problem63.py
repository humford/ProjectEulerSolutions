import time
import math

def powerfuldigitcounts():
    count = 0
    for i in range(1, 10):
        for e in range(1, 100):
            if len(str(i ** e)) == e:
                count += 1
    return count

start = time.time()
answer = powerfuldigitcounts()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
