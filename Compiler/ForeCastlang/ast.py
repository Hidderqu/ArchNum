import visitor

class ASTNode(object):
	"""docstring for ASTNode"""
	def __init__(self):
		super(ASTNode, self).__init__()
		self.name = "Node"

	def __str__(self):
		print ("Node : {}".format(self.name))

	def visit(self, visitor):
		return(self.name)

# ------------- Declarations ------------ #

class Declaration(ASTNode):
	"""docstring for Declaration"""
	def __init__(self):
		super(Declaration, self).__init__()

class windDecl(Declaration):
	"""docstring for windDecl"""
	def __init__(self, identifier, params):
		super(windDecl, self).__init__()
		self.name = "windDecl"
		self.identifier = identifier
		self.params = params

class sunDecl(Declaration):
	"""docstring for sunDecl"""
	def __init__(self, identifier, params):
		super(sunDecl, self).__init__()
		self.name = "sunDecl"
		self.identifier = identifier
		self.params = params

class cloudDecl(Declaration):
	"""docstring for cloudDecl"""
	def __init__(self, identifier, params):
		super(cloudDecl, self).__init__()
		self.name = "cloudDecl"
		self.identifier = identifier
		self.params = params

class RFDecl(Declaration):
	"""docstring for RFDecl"""
	def __init__(self, identifier, params):
		super(RFDecl, self).__init__()
		self.name = "RFDecl"
		self.identifier = identifier
		self.params = params


class Parameter(ASTNode):
	"""docstring for Parameter"""
	def __init__(self, kind, value):
		super(Parameter, self).__init__()
		self.name = kind
		self.value = value
		
		

# ------------- ? ------------ #

class Type(ASTNode):
	"""docstring for Type"""
	def __init__(self):
		super(Type, self).__init__()

class ArrayOf(Type):
	"""docstring for ArrayOf"""
	def __init__(self, size, typeOfElements):
		super(ArrayOf, self).__init__()
		self.size = size
		self.typeOfElements = typeOfElements
		
	
# ------------- Statements ------------ #

class Statement(ASTNode):
	"""docstring for Statement"""
	def __init__(self):
		super(Statement, self).__init__()

# ------------- Statements ------------ #

# ------------- Statements ------------ #
