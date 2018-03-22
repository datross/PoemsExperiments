class Center:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __iter__(self):
		return self

    # def __next__(self)
    #     if self.current > self.high:
    #         raise StopIteration
    #     else:
    #         self.current += 1
    #         return self.current - 1