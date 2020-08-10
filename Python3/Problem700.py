import math
import time

def eulercoin(n):
    return (1504170715041707 * n) % 4503599627370517

def eulercoin_counter():
    smallest = 1504170715041707 + 1

    eulercoins = []
    for i in range(4503599627370517):
        e = eulercoin(i)
        if e < smallest:
            smallest = e
            eulercoins.append(e)

    return sum(eulercoins)


start = time.time()
answer = eulercoin_counter()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
