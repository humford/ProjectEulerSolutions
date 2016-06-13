def distinctTerms(amax, bmax):
	terms = []
	for a in range(2, amax+1):
		for b in range(2, bmax+1):
			terms.append(a ** b)
	return len(set(terms))

print(distinctTerms(100,100))