import time

def champernownesConstant(digit):
	champernowne = ""
	count = 1
	while len(champernowne) < digit:
		champernowne += str(count)
		count += 1
	return champernowne

def evalExpression():
	c = champernownesConstant(1000000)
	c = [int(d) for d in c]
	return c[0] * c[9] * c[99] * c[999] * c[9999] * c[99999] * c[999999]


start = time.time()
answer = evalExpression()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")