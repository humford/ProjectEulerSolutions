def selfpower(n):
    power = 0
    for x in range(1, n + 1):
        power += (x ** x)
    return power


print(selfpower(1000))
