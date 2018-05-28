import sys
from indent import Indent
import ast


class Parser:

    TYPE = ['WIND', 'RAINFALL', 'SUN', 'CLOUD']
    STATEMENT_STARTERS = ['SEMICOLON', 'IDENTIFIER', 'IN', 'AT','MAP']
    DIR = ['NORTH','SOUTH','EAST','WEST']
    TYPE_CLOUD = ['CIRRUS','CUMULUS','CUMULONIMBUS']
    TYPE_RAINFALL = ['PLUIE','NEIGE']
    TYPE_INTENS = ['FORTE', 'FAIBLE', 'NORMALE']

    ALL_VAR = ['TYPE_CLOUD','POSITION','DUREE','INTENSITE','UV','TYPE_RAIN','VITESSE','DIRECTION']
    CLOUD = ['TYPE_CLOUD','POSITION','DUREE']
    SUN = ['UV','POSITION','DUREE']
    WIND = ['VITESSE','DIRECTION','POSITION','DUREE']
    RAINFALL = ['TYPE_RAIN','POSITION','DUREE','INTENSITE']

    REL_OP = ['DOT', 'MOVE', 'ASSIGN', 'COLON','DEL']


    def __init__(self, verbose=False):
        self.indentator = Indent(verbose)
        self.tokens = []
        self.errors = 0

    def show_next(self, n=1):
        try:
            return self.tokens[n - 1]
        except IndexError:
            print('ERROR: no more tokens left!')
            sys.exit(1)

    def expect(self, kind):
        actualToken = self.show_next()
        actualKind = actualToken.kind
        actualPosition = actualToken.position
        if actualKind == kind:
            return self.accept_it()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(actualPosition), kind, actualKind))
            sys.exit(1)

    # same as expect() but no error if not correct kind
    def maybe(self, kind):
        if self.show_next().kind == kind:
            return self.accept_it()

    def accept_it(self):
        token = self.show_next()
        output = str(token.kind) + ' ' + token.value
        self.indentator.say(output)
        return self.tokens.pop(0)

    def remove_comments(self):
        result = []
        in_comment = False
        for token in self.tokens:
            if token.kind == 'COMMENT':
                pass
            elif token.kind == 'LCOMMENT':
                in_comment = True
            elif token.kind == 'RCOMMENT':
                in_comment = False
            else:
                if not in_comment:
                    result.append(token)
        return result

    def parse(self, tokens):
        self.tokens = tokens
        self.tokens = self.remove_comments()
        return self.parse_program()

    def parse_program(self):
        program = []
        self.indentator.indent('Parsing Program')
        declarations = self.parse_declarations()
        program.append(declarations)
        
        self.expect('MAIN')
        stats = self.parse_statements()
        program.append(stats)
        self.indentator.dedent()

        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

        return program

    def parse_declarations(self):
        declarations = []
        self.indentator.indent('Parsing Declarations')
        while self.show_next().kind == 'IDENTIFIER':
            varName = self.show_next().value
            self.accept_it()
            aDecl = self.parse_declaration(varName)
            declarations.append(aDecl)
        self.indentator.dedent()

        return declarations

    def parse_declaration(self, varName):
        self.indentator.indent('Parsing Declaration of {}'.format(varName))
        self.expect('ASSIGN')
        if self.show_next().kind == 'WIND':
            self.accept_it()
            aDecl = self.parse_wind(varName)
        elif self.show_next().kind == 'SUN':
            self.accept_it()
            aDecl = self.parse_sun(varName)
        elif self.show_next().kind == 'CLOUD':
            self.accept_it()
            aDecl = self.parse_cloud(varName)
        elif self.show_next().kind == 'RAINFALL':
            self.accept_it()
            aDecl = self.parse_rainfall(varName)
        self.indentator.dedent()

        return [aDecl]

    def parse_wind(self, varName):
        self.indentator.indent('Parsing Wind')
        self.expect('LBRACE')
        params = self.parse_vars_wind()
        self.expect('RBRACE')
        windDecl = ast.windDecl(varName, params)
        self.indentator.dedent()

        return [windDecl]

    def parse_vars_wind(self):
        params = []
        self.indentator.indent('Parsing Vars_wind')
        if self.show_next().kind in self.WIND:
            param = self.parse_var_wind()
            params.append(param)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            param = self.parse_var_wind()
            params.append(param)
        self.indentator.dedent()

        return [params]

    def parse_var_wind(self):
        self.indentator.indent('Parsing Var_wind')
        if self.show_next().kind == 'POSITION':
            param = self.parse_position()
        elif self.show_next().kind == 'VITESSE':
            param = self.parse_vitesse()
        elif self.show_next().kind == 'DUREE':
            param = self.parse_duree()
        elif self.show_next().kind == 'DIRECTION':
            param = self.parse_direction()
        self.indentator.dedent()

        return [param]

    def parse_sun(self, varName):
        self.indentator.indent('Parsing Sun')
        self.expect('LBRACE')
        params = self.parse_vars_sun()
        self.expect('RBRACE')
        sunDecl = ast.sunDecl(varName, params)
        self.indentator.dedent()

        return [sunDecl]

    def parse_vars_sun(self):
        params = []
        self.indentator.indent('Parsing Vars_sun')
        if self.show_next().kind in self.SUN:
            param = self.parse_var_sun()
            params.append(param)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            param = self.parse_var_sun()
            params.append(param)
        self.indentator.dedent()

        return params

    def parse_var_sun(self):
        self.indentator.indent('Parsing Var_sun')
        if self.show_next().kind == 'POSITION':
            param = self.parse_position()
        elif self.show_next().kind == 'UV':
            param = self.parse_uv()
        elif self.show_next().kind == 'DUREE':
            param = self.parse_duree()
        self.indentator.dedent()

        return [param]

    def parse_cloud(self, varName):
        self.indentator.indent('Parsing Cloud')
        self.expect('LBRACE')
        params = self.parse_vars_cloud()
        self.expect('RBRACE')
        cloudDecl = ast.cloudDecl(varName, params)
        self.indentator.dedent()

        return [cloudDecl]

    def parse_vars_cloud(self):
        params = []
        self.indentator.indent('Parsing Vars_cloud')
        if self.show_next().kind in self.CLOUD:
            param = self.parse_var_cloud()
            params.append(param)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            param = self.parse_var_cloud()
            params.append(param)
        self.indentator.dedent()

        return [params]

    def parse_var_cloud(self):
        self.indentator.indent('Parsing Var_cloud')
        if self.show_next().kind == 'POSITION':
            param = self.parse_position()
        elif self.show_next().kind == 'TYPE_CLOUD':
            param = self.parse_type_cloud()
        elif self.show_next().kind == 'DUREE':
            param = self.parse_duree()
        self.indentator.dedent()

        return [param]

    def parse_rainfall(self, varName):
        self.indentator.indent('Parsing Rainfall')
        self.expect('LBRACE')
        params = self.parse_vars_rainfall()
        self.expect('RBRACE')
        RFDecl = ast.RFDecl(varName, params)
        self.indentator.dedent()

        return [RFDecl]

    def parse_vars_rainfall(self):
        params = []
        self.indentator.indent('Parsing Vars_rainfall')
        if self.show_next().kind in self.RAINFALL:
            param = self.parse_var_rainfall()
            params.append(param)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            param = self.parse_var_rainfall()
            params.append(param)
        self.indentator.dedent()

        return [params]

    def parse_var_rainfall(self):
        self.indentator.indent('Parsing Var_rainfall')
        if self.show_next().kind == 'POSITION':
            param = self.parse_position()
        elif self.show_next().kind == 'INTENSITE':
            param = self.parse_intensite()
        elif self.show_next().kind == 'DUREE':
            param = self.parse_duree()
        elif self.show_next().kind == 'TYPE_RAIN':
            param = self.parse_type_rainfall()
        self.indentator.dedent()

        return [param]

    def parse_direction(self):
        self.indentator.indent('Parsing Direction')
        self.expect('DIRECTION')
        self.expect('COLON')
        if self.show_next().kind in self.DIR:
            value = self.show_next().value
            self.accept_it()
            param = ast.Parameter("direction", value)
        self.indentator.dedent()

        return [param]

    def parse_duree(self):
        self.indentator.indent('Parsing Duree')
        self.expect('DUREE')
        self.expect('COLON')
        value = self.show_next().value
        self.expect('INT')
        param = ast.Parameter("duree", value)
        self.indentator.dedent()

        return [param]

    def parse_position(self):
        self.indentator.indent('Parsing Position')
        self.expect('POSITION')
        self.expect('COLON')
        value = self.parse_coord()
        param = ast.Parameter("position", value)
        self.indentator.dedent()

        return [param]

    def parse_coord(self):
        self.indentator.indent('Parsing Coordinates')
        self.expect('LPAREN')
        valueX = self.show_next().value
        self.expect('INT')
        self.expect('COMMA')
        valueY = self.show_next().value
        self.expect('INT')
        self.expect('RPAREN')
        self.indentator.dedent()

        return (valueX, valueY)

    def parse_vitesse(self):
        self.indentator.indent('Parsing Vitesse')
        self.expect('VITESSE')
        self.expect('COLON')
        value = self.show_next().value
        self.expect('INT')
        param = ast.Parameter("vitesse", value)
        self.indentator.dedent()

        return [param]

    def parse_type_cloud(self):
        self.indentator.indent('Parsing Type_could')
        self.expect('TYPE_CLOUD')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_CLOUD:
            value = self.show_next().value
            self.accept_it()
            param = ast.Parameter("typeCloud", value)
        self.indentator.dedent()

        return [param]
	
    def parse_type_rainfall(self):
        self.indentator.indent('Parsing Type_rainfall')
        self.expect('TYPE_RAIN')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_RAINFALL:
            value = self.show_next().value
            self.accept_it()
            param = ast.Parameter("typeRain", value)
        self.indentator.dedent()

        return [param]

    def parse_uv(self):
        self.indentator.indent('Parsing Uv')
        self.expect('UV')
        self.expect('COLON')
        value = self.show_next().value
        self.expect('INT')
        param = ast.Parameter("uv", value)
        self.indentator.dedent()

        return [param]

    def parse_intensite(self):
        self.indentator.indent('Parsing Intensite')
        self.expect('INTENSITE')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_INTENS:
            value = self.show_next().value
            self.accept_it()
            param = ast.Parameter("intensite", value)
        self.indentator.dedent()

        return [param]


    def parse_statements(self):
        statements = []
        self.indentator.indent('Parsing Statements')
        while self.show_next().kind in self.STATEMENT_STARTERS:
            statement = self.parse_statement()
            statements.append(statement)
        self.expect('ENDMAIN')
        self.indentator.dedent()

        return statements

    def parse_statement(self):
        
        self.indentator.indent('Parsing Statement')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it()
        elif self.show_next().kind == 'IDENTIFIER':
            statement = self.parse_expression()
        elif self.show_next().kind == 'AT':
            statement = self.parse_atstatement()
        elif self.show_next().kind == 'IN':
            statement = self.parse_instatement()
        elif self.show_next().kind == 'MAP':
            statement = self.parse_map()
        self.indentator.dedent()

        return [statement]

        #####
        
    def parse_atstatement(self):
        self.indentator.indent('Parsing AtStatement')
        self.expect('AT')
        self.expect('BAR')
        time = self.show_next().value
        self.expect('INT')
        atStat = [ast.atStatement(time)]
        self.expect('LBRACKET')
        exp = self.parse_expression()
        atStat.append(exp)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            exp = self.parse_expression()
            atStat.append(exp)
        self.expect('RBRACKET')
        self.indentator.dedent()

        return atStat
        
    def parse_instatement(self):
        self.indentator.indent('Parsing InStatement')
        self.expect('IN')
        self.expect('BAR')
        start = self.show_next().value
        self.expect('INT')
        self.expect('SUB')
        finish = self.show_next().value
        self.expect('INT')
        inStat = [ast.inStatement(start, finish)]
        self.expect('LBRACKET')
        exp = self.parse_expression()
        inStat.append(exp)
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            exp = self.parse_expression()
            inStat.append(exp)
        self.expect('RBRACKET')
        self.indentator.dedent()

        return inStat

    def parse_map(self):
        self.indentator.indent('Parsing Map')
        self.expect('MAP')
        self.expect('LBRACKET')
        displayed = []
        while(self.show_next().kind == 'IDENTIFIER'):
            displayed.append(self.show_next().value)
            self.accept_it()
            if self.show_next().kind == 'SEMICOLON':
            	self.accept_it()  
        self.expect('DBAR')
        longit = self.show_next().value
        self.expect('LATLONG')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it()
        latit = self.show_next().value  
        self.expect('LATLONG')
        longlat = (longit, latit)
        self.expect('DBAR')
        dimX = self.show_next().value  
        self.expect('INT')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it() 
        dimY = self.show_next().value  
        self.expect('INT')
        dims = (dimX, dimY)
        self.expect('RBRACKET')
        self.indentator.dedent()

        return [ast.mapStatement(displayed, longlat, dims)]


    def parse_expression(self):
        self.indentator.indent('Parsing Expression')
        ident = self.show_next().value
        self.expect('IDENTIFIER')
        exp = ast.Expression(ident)
        ope = self.parse_term()
        self.indentator.dedent()

        return [exp, ope]
     
        
            
    def parse_term(self):
        self.indentator.indent('Parsing Term')
        if self.show_next().kind == 'DOT':
            ope = self.parse_dot()
        elif self.show_next().kind == 'ASSIGN':
            ope = self.parse_declaration()
        elif self.show_next().kind == 'DEL':
            ope = self.accept_it()
        elif self.show_next().kind == 'MOVE':
            ope = self.parse_move()	
        self.indentator.dedent()
        
        return ope
        
    def parse_dot(self):
        self.indentator.indent('Parsing dot')
        self.expect('DOT')
        if self.show_next().kind == 'POSITION':
            param = self.parse_position()
        elif self.show_next().kind == 'INTENSITE':
            param = self.parse_intensite()
        elif self.show_next().kind == 'DUREE':
            param = self.parse_duree()
        elif self.show_next().kind == 'TYPE_RAINFALL':
            param = self.parse_type_rainfall()
        elif self.show_next().kind == 'TYPE_CLOUD':
            param = self.parse_type_cloud()
        elif self.show_next().kind == 'DIRECTION':
            param = self.parse_direction()
        elif self.show_next().kind == 'VITESSE':
            param = self.parse_vitesse()
        self.indentator.dedent()

        return [ast.dotOperation(), param]
        
    def parse_move(self):
        self.indentator.indent('Parsing move')
        self.expect('MOVE')
        coords = self.parse_coord()
        param = ast.Parameter("position", coords)
        self.indentator.dedent()

        return [ast.moveOperation(), param]
