import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

count = 0
for n in range(1, 101):
    for r in range(1, n):
        c = nCr(n,r)
        if c > 1000000:
            count += 1
print(count)
