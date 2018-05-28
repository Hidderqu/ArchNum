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
		
	
# ------------- Statements ------------ #

class Statement(ASTNode):
	"""docstring for Statement"""
	def __init__(self):
		super(Statement, self).__init__()

class inStatement(Statement):
	"""docstring for inStatement"""
	def __init__(self, start, end):
		super(inStatement, self).__init__()
		self.start = start
		self.end = end

class atStatement(Statement):
	"""docstring for atStatement"""
	def __init__(self, time):
		super(atStatement, self).__init__()
		self.time = time
		
class mapStatement(Statement):
	"""docstring for mapStatement"""
	def __init__(self, displayed, longlat, dims):
		super(mapStatement, self).__init__()
		self.displayed = displayed
		self.longlat = longlat
		self.dims = dims


# ------------- Expressions ------------ #

class Expression(ASTNode):
	"""docstring for Expression"""
	def __init__(self, identifier):
		super(Expression, self).__init__()
		self.identifier = identifier

# ------------- Operations ------------ #

class Operation(ASTNode):
	"""docstring for Operation"""
	def __init__(self):
		super(Operation, self).__init__()

class dotOperation(Operation):
	"""docstring for dotOperation"""
	def __init__(self):
		super(dotOperation, self).__init__()
		
class assignOperation(Operation):
	"""docstring for assignOperation"""
	def __init__(self):
		super(assignOperation, self).__init__()

class delOperation(Operation):
	"""docstring for delOperation"""
	def __init__(self):
		super(delOperation, self).__init__()

class moveOperation(Operation):
	"""docstring for moveOperation"""
	def __init__(self):
		super(moveOperation, self).__init__()
		

		