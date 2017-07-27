import time
import math

mod = 10000000000
core = 2 ** 7830457
core = 28433 * core + 1

start = time.time()
answer = core % mod
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
