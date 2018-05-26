class Visitor(object):
	"""docstring for Visitor"""
	def __init__(self):
		super(Visitor, self).__init__()
		
	def showAST(self, ast):
		for Node in ast:
			Node.visit()