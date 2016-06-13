def reciprocalCycle(d):
	r = []
	for x in range(2, d+1):
		r.append(float(1/x))
	return r

print(reciprocalCycle(1000))