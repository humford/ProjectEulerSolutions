def fibonacci(maxVal):
    fib = []
    x = 1
    y = 2
    while y < maxVal:
        fib.extend([x, y])
    x += y
    y += x
    return fib


def evenFib(maxVal):
    s = []
    for i in fibonacci(maxVal):
        if i % 2 == 0:
            s.append(i)
    print(sum(s))


evenFib(4000000)
