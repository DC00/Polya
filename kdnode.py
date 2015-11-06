class kdnode:
	def __init__(self):
		self.dim = -1
		self.val = -1
		self.st = -1
		self.end = -1
		self.dist = 0
		self.lessChild = 0
		self.greaterChild = 0
		self.minx = -9999
		self.miny = -9999
		self.width = -9999
		self.height = -9999

	def __lt__(self, other):
		return self.dist < other.dist;
		
	def __gt__(self, other):
		return self.dist > other.dist;
		
	def __eq__(self, other):
		return self.dist == other.dist;
		
	def __le__(self, other):
		return self.dist <= other.dist;
		
	def __ge__(self, other):
		return self.dist >= other.dist;
		
	def __ne__(self, other):
		return self.dist != other.dist;
