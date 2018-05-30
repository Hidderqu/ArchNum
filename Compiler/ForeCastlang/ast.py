import visitor

class ASTNode(object):
	"""docstring for ASTNode"""
	def __init__(self):
		super(ASTNode, self).__init__()

	def __str__(self):
		print ("Node : {}".format(self.name))

	def accept(self, visitor):
		#on recupere le nom de la classe  specialisee de l'AST
		className = self.__class__.__name__
		#on recupere la methode du visitor qui se nomme visit_<className>
		func = getattr(visitor, 'visit_' + className)
		#on appelle la methode avec le noeud de l'ast courrant en parametre
		return func(self)


# ------------- Program ------------ #
class Program(ASTNode):
	"""docstring for Program"""
	def __init__(self, declarations, statements):
		super(Program, self).__init__()
		self.declarations = declarations
		self.statements = statements

# ------------- Declarations ------------ #

class Declaration(ASTNode):
	"""docstring for Declaration"""
	def __init__(self):
		super(Declaration, self).__init__()

class windDecl(Declaration):
	"""docstring for windDecl"""
	def __init__(self, identifier, params):
		super(windDecl, self).__init__()
		self.identifier = identifier
		self.params = params

class sunDecl(Declaration):
	"""docstring for sunDecl"""
	def __init__(self, identifier, params):
		super(sunDecl, self).__init__()
		self.identifier = identifier
		self.params = params

class cloudDecl(Declaration):
	"""docstring for cloudDecl"""
	def __init__(self, identifier, params):
		super(cloudDecl, self).__init__()
		self.identifier = identifier
		self.params = params

class RFDecl(Declaration):
	"""docstring for RFDecl"""
	def __init__(self, identifier, params):
		super(RFDecl, self).__init__()
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
	def __init__(self, start, end, expressions):
		super(inStatement, self).__init__()
		self.start = start
		self.end = end
		self.expressions = expressions

class atStatement(Statement):
	"""docstring for atStatement"""
	def __init__(self, time, expressions):
		super(atStatement, self).__init__()
		self.time = time
		self.expressions = expressions
		
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
	def __init__(self, identifier, operation):
		super(Expression, self).__init__()
		self.identifier = identifier
		self.operation = operation

# ------------- Operations ------------ #

class Operation(ASTNode):
	"""docstring for Operation"""
	def __init__(self):
		super(Operation, self).__init__()

class dotOperation(Operation):
	"""docstring for dotOperation"""
	def __init__(self, param):
		super(dotOperation, self).__init__()
		self.param = param
		
class assignOperation(Operation):
	"""docstring for assignOperation"""
	def __init__(self, decl):
		super(assignOperation, self).__init__()
		self.decl = decl

class delOperation(Operation):
	"""docstring for delOperation"""
	def __init__(self):
		super(delOperation, self).__init__()

class moveOperation(Operation):
	"""docstring for moveOperation"""
	def __init__(self, coord_param):
		super(moveOperation, self).__init__()
		self.coords = coord_param
		

		