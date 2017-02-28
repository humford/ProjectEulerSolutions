import math


def largestPrimeFactor(n=600851475143):
    for i in range(2, int(math.sqrt(n) + 1)):
        while n % i == 0:
            n //= i
            print("Yay, %d is a factor, now we should test %d" % (i, n))
            if n == 1 or n == i:
                return i


print(largestPrimeFactor())
