def palidrome(n):
	n = list(str(n))
	for i, x in zip(n, reversed(n)):
		if i != x:
			return False
	else:
		return True

def largestPalindrome():
	l = 0
	for n1 in range(999,99,-1):
		for n2 in range(999,99,-1):
			if palidrome(n1*n2):
				if n1*n2 > l:
					l = n1*n2
	return l

print largestPalindrome() 