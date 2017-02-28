def lychrelNumbersBelow(n):
	lychrelNumbers = []
	for x in range(1,n+1):
		if lychrel(x): lychrelNumbers.append(x)
	return lychrelNumbers

def lychrel(n):
	for i in range(1, 50):
		n += int(str(n)[::-1])
		if palindromic(n):
			return False
	return True
					

def palindromic(n):
	return (n == int(str(n)[::-1]))

print len(lychrelNumbersBelow(10000))