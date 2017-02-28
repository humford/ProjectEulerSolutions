import math

def factorialDigitSum(n): return sum([int(x) for x in str(math.factorial(n))])

print factorialDigitSum(100)