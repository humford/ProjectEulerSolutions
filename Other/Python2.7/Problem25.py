def fibonacciDig(digits):
	x = 1
	y = 2
	fib = [1, x, y]
	while(True):
		x = x + y
		fib.append(x)
		if x > digits:
			return fib.index(x)+1
		y = y + x
		fib.append(y)
		if y > digits:
			return fib.index(y)+1

num = 10 ** 999
print(fibonacciDig(num))
