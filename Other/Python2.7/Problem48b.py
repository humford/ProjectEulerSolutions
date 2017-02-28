def selfpower(n):
	result = long(0)
	modulo = long(10000000000)
	for x in range(1, n+1):
		temp = long(i)
		for j in range(1, i+1):
			temp *= i
			if temp >= (long.MaxValue / 1000):
				temp %= modulo
	result += temp
	
		power += (x ** x)
	return power

print(selfpower(1000))
