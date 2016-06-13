def digits(n):
	return [int(i) for i in str(n)]

def digitnthPowers(n):
	powers = []
	
	for x in range(2, 355000):
		if sum([d**n for d in digits(x)]) == x:
			powers.append(x)
	return sum(powers), powers

print(digitnthPowers(5))