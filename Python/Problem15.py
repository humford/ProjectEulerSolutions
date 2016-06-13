class Grid(object):
	"""docstring for Grid"""
	def __init__(self, length):
		self.length = length
		self.height = length

	def createGrid(self):
		grid = []
		for r in xrange(0, self.length):
			grid.append([])
			for c in xrange(0, self.height):
				grid[r].append(0)
		return grid

def main():
	searchGrid = Grid(20)
	problemGrid = searchGrid.createGrid()
	for x in 






