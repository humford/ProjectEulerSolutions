def smallestMultiple(n):
    i = n
    while True:
        for x in range(1, n + 1):
            if i % x != 0:
                break
            elif x == n:
                return i
        i += 1


print(smallestMultiple(20))
