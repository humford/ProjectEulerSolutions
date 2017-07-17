import time

def digitsum(n):
    total = 0
    for digit in str(n):
        total += int(digit)
    return total

def powerfuldigitsum(limit):
    largestdigitsum = 0
    for a in range(limit+1):
        for b in range(limit+1):
            test = a ** b
            if digitsum(test) > largestdigitsum:
                largestdigitsum = digitsum(test)
    return largestdigitsum

start = time.time()
answer = powerfuldigitsum(100)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
