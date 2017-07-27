import time
import math

#how many reversible numbers are there under 1 billion
#reversible(n) == [ n + reverse(n) ] all odd digits
def reverse(n):
    n = list(str(n))
    reverse = ''
    for d in reversed(n):
        reverse += d
    return int(reverse)

def reverse1(n):
    flag = n
    rev = 0
    while int(flag):
        rem = int(flag % 10)
        rev *= 10
        rev += rem
        flag /= 10
    return int(rev)

def reversible(n):
    if len(str(n)) != len(str(reverse(n))):
        return False
    for i in str(n + reverse(n)):
        if int(i) % 2 == 0:
            return False
    return True

def count_reversible(limit):
    count = 0
    for n in range(1, limit+1, 2):
        if reversible(n):
            count += 2
    return count

def count_reversible_fast(digits):
    count = 0
    for i in range(1, digits+1):
        if i % 2 == 0:
            count += 20 * pow(30, i // 2 - 1)
        elif i % 4 == 3:
            count += 100 * pow(500, i // 4)
    return count

start = time.time()
answer = count_reversible_fast(9)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
