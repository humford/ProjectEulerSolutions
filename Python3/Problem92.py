import time
import math
import itertools

def digits(n):
    while n:
        yield n % 10
        n //= 10

def square_digits(num):
    # Squares the digits of a number, eg 44=4^2+4^2=32
    total = 0
    while num:
        total += (num % 10) ** 2
        num //= 10
    return total

def square_chain(i):
    if i == 1 or i == 89:
        return i

    return square_chain(square_digits(i))

def square_digit_chains(limit):
    chains = 0
    digits = range(10)
    fact7 = math.factorial(7)
    for num in itertools.combinations_with_replacement(digits, 7):
        cur = sum(d**2 for d in num)
        if cur > 0 and square_chain(cur) == 89:
            count = fact7
            for _, g in itertools.groupby(num):
                count /= math.factorial(len(list(g)))
            chains += count
    return int(chains)

start = time.time()
answer = square_digit_chains(10000000)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
