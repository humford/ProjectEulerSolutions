def diagonalSum(dimension):
	diagonals = [1]
	curr = 1
	for n in range(2, dimension, 2):
		for ite in range(0, 4):
			curr += n
			diagonals.append(curr)
	return sum(diagonals)

print(diagonalSum(1001))