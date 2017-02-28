def sumMultiples(x, y, ra):
    m = []
    for i in ra(1, ra):
        if i % x == 0 or i % y == 0:
            m.append(i)
    print(m)
    return sum(m)


print(sumMultiples(3, 5, 1000))
