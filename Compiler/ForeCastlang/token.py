class Token:

	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __str__(self):
		return ("Token : Kind - {} / Value - {} / Position - {}".format(self.kind, self.value, self.position))