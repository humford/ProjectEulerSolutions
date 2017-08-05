import time
import math
import re

def is_concealed_square(n):
    p = re.compile('1\d2\d3\d4\d5\d6\d7\d8\d9\d0')
    if p.findall(str(n)):
        return True
    return False

def concealed_square():
    for i in range(3 * 10 ** 9, int(3.2 * 10 ** 9), 100):
        if is_concealed_square(i + 30  ** 2):
            return i
        if is_concealed_square((i + 70) ** 2):
            return i + 70
    return 0

def match(n):
    s = str(n)
    return not all(int(s[x*2]) == x+1 for x in range(9))

def concealed_square1():
    n = 138902663    # sqrt(19293949596979899)
    while match(n*n): n -= 2
    return n*10

start = time.time()
answer = concealed_square1()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
