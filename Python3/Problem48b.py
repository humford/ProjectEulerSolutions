def selfpower(n, power=None):
    result = int(0)
    modulo = int(10000000000)
    for i in range(1, n + 1):
        temp = int(i)
        for j in range(1, i + 1):
            temp *= i
            if temp >= (int.MaxValue / 1000):
                temp %= modulo
    result += temp
    power += (i ** i)
    return power

print(selfpower(1000))
