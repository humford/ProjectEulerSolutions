def d(n):
    s = 0
    for x in range(1, n):
        if n % x == 0: s += x
    return s

def amicableNumbersUnder(m):
    amicableNumbers = []
    for x in range(1, m+1):
        if d(d(x)) == x and d(x) != x:
            if x not in amicableNumbers:
                amicableNumbers.append(x)
                amicableNumbers.append(d(x))
    print(amicableNumbers)
    return amicableNumbers

print sum(amicableNumbersUnder(10000))