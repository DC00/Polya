class point:
	def __init__(self, x, y):
		self.x  = x;
		self.y = y;
		self.angle = -9999;

	def __getitem__(self, key):
		if key == 0:
			return self.x
		if key == 1:
			return self.y

