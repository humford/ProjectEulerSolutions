import math
import collections

def sum_digits3(n):
   r = 0
   while n:
       r, n = r + n % 10, n // 10
   return r

def ASieve(limit):
	is_prime = list()
	is_prime = [False] * (limit+1)

	for x in range(1, int(math.sqrt(limit))+1):
		for y in range(1, int(math.sqrt(limit))+1):
			
			n = 4*x**2 + y**2
			if n <= limit and (n%12==1 or n%12==5):
				is_prime[n] = not is_prime[n]

			n = 3*x**2+y**2
			if n <= limit and n%12==7:
				is_prime[n] = not is_prime[n]

			n = 3*x**2-y**2
			if x > y and n <= limit and n%12==11:
				is_prime[n] = not is_prime[n]

	for n in range(5, int(math.sqrt(limit))):
		if is_prime[n]:
			for k in range(n**2, limit+1, n**2):
				is_prime[k] = False

	return is_prime

def find4DigPrimes():
	r = ASieve(10000)
	result = []
	for x in range(1000, len(r)):
		if r[x]:
			result.append(x)
	return result

def findArith():
	r = find4DigPrimes()
	possible = []
	for x in r:
		for i in range((x if x < 5000 else 5000), 0, -10):
			if (((x+i) in r) and ((x+2*i) in r)) and (sum_digits3(x)==sum_digits3(x+i)==sum_digits3(x+2*i)):
				possible.append([x, x+i, x+2*i])
	return possible

print(findArith())