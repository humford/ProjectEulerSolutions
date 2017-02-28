import math

class Grid(object):
	"""docstring for Grid"""
	def __init__(self, length, height):
		self.length = length
		self.height = height

	def createGrid(self):
		grid = []
		for r in xrange(0, self.length):
			grid.append([])
			for c in xrange(0, self.height):
				grid[r].append(0)
		return grid

def main():
	searchGrid = Grid(20, 20)
	problemGrid = searchGrid.createGrid()
	return problemGrid

def combinatoricsPaths(n):
	return math.factorial(2 * n) / (math.factorial(n) ** 2)

print combinatoricsPaths(20)






