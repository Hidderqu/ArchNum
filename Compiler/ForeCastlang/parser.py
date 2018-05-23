import sys
from indent import Indent


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
        self.parse_program()

    def parse_program(self):
        self.indentator.indent('Parsing Program')
        self.parse_declarations()
        self.expect('MAIN')
        self.parse_statements()
        self.indentator.dedent()

        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

    def parse_declarations(self):
        self.indentator.indent('Parsing Declarations')
        while self.show_next().kind == 'IDENTIFIER':
            self.accept_it()
            self.parse_declaration()
        self.indentator.dedent()

    def parse_declaration(self):
        self.indentator.indent('Parsing Declaration')
        self.expect('ASSIGN')
        if self.show_next().kind == 'WIND':
            self.accept_it()
            self.parse_wind()
        elif self.show_next().kind == 'SUN':
            self.accept_it()
            self.parse_sun()
        elif self.show_next().kind == 'CLOUD':
            self.accept_it()
            self.parse_cloud()
        elif self.show_next().kind == 'RAINFALL':
            self.accept_it()
            self.parse_rainfall()
        self.indentator.dedent()

    def parse_wind(self):
        self.indentator.indent('Parsing Wind')
        self.expect('LBRACE')
        self.parse_vars_wind()
        self.expect('RBRACE')
        self.indentator.dedent()

    def parse_vars_wind(self):
        self.indentator.indent('Parsing Vars_wind')
        if self.show_next().kind in self.WIND:
            self.parse_var_wind()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_var_wind()
        self.indentator.dedent()

    def parse_var_wind(self):
        self.indentator.indent('Parsing Var_wind')
        if self.show_next().kind == 'POSITION':
            self.parse_position()
        elif self.show_next().kind == 'VITESSE':
            self.parse_vitesse()
        elif self.show_next().kind == 'DUREE':
            self.parse_duree()
        elif self.show_next().kind == 'DIRECTION':
            self.parse_direction()
        self.indentator.dedent()

    def parse_sun(self):
        self.indentator.indent('Parsing Sun')
        self.expect('LBRACE')
        self.parse_vars_sun()
        self.expect('RBRACE')
        self.indentator.dedent()

    def parse_vars_sun(self):
        self.indentator.indent('Parsing Vars_sun')
        if self.show_next().kind in self.SUN:
            self.parse_var_sun()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_var_sun()
        self.indentator.dedent()

    def parse_var_sun(self):
        self.indentator.indent('Parsing Var_sun')
        if self.show_next().kind == 'POSITION':
            self.parse_position()
        elif self.show_next().kind == 'UV':
            self.parse_uv()
        elif self.show_next().kind == 'DUREE':
            self.parse_duree()
        self.indentator.dedent()

    def parse_cloud(self):
        self.indentator.indent('Parsing Cloud')
        self.expect('LBRACE')
        self.parse_vars_cloud()
        self.expect('RBRACE')
        self.indentator.dedent()

    def parse_vars_cloud(self):
        self.indentator.indent('Parsing Vars_cloud')
        if self.show_next().kind in self.CLOUD:
            self.parse_var_cloud()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_var_cloud()
        self.indentator.dedent()

    def parse_var_cloud(self):
        self.indentator.indent('Parsing Var_cloud')
        if self.show_next().kind == 'POSITION':
            self.parse_position()
        elif self.show_next().kind == 'TYPE_CLOUD':
            self.parse_type_cloud()
        elif self.show_next().kind == 'DUREE':
            self.parse_duree()
        self.indentator.dedent()

    def parse_rainfall(self):
        self.indentator.indent('Parsing Rainfall')
        self.expect('LBRACE')
        self.parse_vars_rainfall()
        self.expect('RBRACE')
        self.indentator.dedent()

    def parse_vars_rainfall(self):
        self.indentator.indent('Parsing Vars_rainfall')
        if self.show_next().kind in self.RAINFALL:
            self.parse_var_rainfall()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_var_rainfall()
        self.indentator.dedent()

    def parse_var_rainfall(self):
        self.indentator.indent('Parsing Var_rainfall')
        if self.show_next().kind == 'POSITION':
            self.parse_position()
        elif self.show_next().kind == 'INTENSITE':
            self.parse_intensite()
        elif self.show_next().kind == 'DUREE':
            self.parse_duree()
        elif self.show_next().kind == 'TYPE_RAIN':
            self.parse_type_rainfall()
        self.indentator.dedent()

    def parse_direction(self):
        self.indentator.indent('Parsing Direction')
        self.expect('DIRECTION')
        self.expect('COLON')
        if self.show_next().kind in self.DIR:
            self.accept_it()
        self.indentator.dedent()

    def parse_duree(self):
        self.indentator.indent('Parsing Duree')
        self.expect('DUREE')
        self.expect('COLON')
        self.expect('INT')
        self.indentator.dedent()

    def parse_position(self):
        self.indentator.indent('Parsing Position')
        self.expect('POSITION')
        self.expect('COLON')
        self.parse_coord()
        
        self.indentator.dedent()

    def parse_coord(self):
        self.indentator.indent('Parsing Coordinates')
        self.expect('LPAREN')
        self.expect('INT')
        self.expect('COMMA')
        self.expect('INT')
        self.expect('RPAREN')
        self.indentator.dedent()

    def parse_vitesse(self):
        self.indentator.indent('Parsing Vitesse')
        self.expect('VITESSE')
        self.expect('COLON')
        self.expect('INT')
        self.indentator.dedent()

    def parse_type_cloud(self):
        self.indentator.indent('Parsing Type_could')
        self.expect('TYPE_CLOUD')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_CLOUD:
            self.accept_it()
        self.indentator.dedent()
	
    def parse_type_rainfall(self):
        self.indentator.indent('Parsing Type_rainfall')
        self.expect('TYPE_RAIN')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_RAINFALL:
            self.accept_it()
        self.indentator.dedent()

    def parse_uv(self):
        self.indentator.indent('Parsing Uv')
        self.expect('UV')
        self.expect('COLON')
        self.expect('INT')
        self.indentator.dedent()

    def parse_intensite(self):
        self.indentator.indent('Parsing Intensite')
        self.expect('INTENSITE')
        self.expect('COLON')
        if self.show_next().kind in self.TYPE_INTENS:
            self.accept_it()
        self.indentator.dedent()


    def parse_statements(self):
        self.indentator.indent('Parsing Statements')
        while self.show_next().kind in self.STATEMENT_STARTERS:
            self.parse_statement()
        self.expect('ENDMAIN')
        self.indentator.dedent()

    """a relier"""


    def parse_statement(self):
        
        self.indentator.indent('Parsing Statement')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it()
        elif self.show_next().kind == 'IDENTIFIER':
            self.parse_expression()
        elif self.show_next().kind == 'AT':
            self.parse_atstatement()
        elif self.show_next().kind == 'IN':
            self.parse_instatement()
        elif self.show_next().kind == 'MAP':
            self.parse_map()
        self.indentator.dedent()
        
        #####
        
    def parse_atstatement(self):
        self.indentator.indent('Parsing AtStatement')
        self.expect('AT')
        self.expect('BAR')
        self.expect('INT')
        self.expect('LBRACKET')
        self.parse_expression()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_expression()
        self.expect('RBRACKET')
        self.indentator.dedent()
        
    def parse_instatement(self):
        self.indentator.indent('Parsing InStatement')
        self.expect('IN')
        self.expect('BAR')
        self.expect('INT')
        self.expect('SUB')
        self.expect('INT')
        self.expect('LBRACKET')
        self.parse_expression()
        while self.show_next().kind == 'SEMICOLON':
            self.accept_it()
            self.parse_expression()
        self.expect('RBRACKET')
        self.indentator.dedent()

    def parse_map(self):
        self.indentator.indent('Parsing Map')
        self.expect('MAP')
        self.expect('LBRACKET')
        while(self.show_next().kind == 'IDENTIFIER'):
            self.accept_it()
            if self.show_next().kind == 'SEMICOLON':
            	self.accept_it()  
        self.expect('DBAR')
        self.expect('LATLONG')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it()  
        self.expect('LATLONG')
        self.expect('DBAR')
        self.expect('INT')
        if self.show_next().kind == 'SEMICOLON':
            self.accept_it() 
        self.expect('INT')
        self.expect('RBRACKET')
        self.indentator.dedent()


    def parse_expression(self):
        self.indentator.indent('Parsing Expression')
        self.expect('IDENTIFIER')
        self.parse_term()
        self.indentator.dedent()
     
        
            
    def parse_term(self):
        self.indentator.indent('Parsing Term')
        if self.show_next().kind == 'DOT':
            self.parse_dot()
        elif self.show_next().kind == 'ASSIGN':
            self.parse_declaration()
        elif self.show_next().kind == 'DEL':
            self.accept_it()
        elif self.show_next().kind == 'MOVE':
            self.parse_move()	
        self.indentator.dedent()
        
        
    def parse_dot(self):
        self.indentator.indent('Parsing dot')
        self.expect('DOT')
        if self.show_next().kind == 'POSITION':
            self.parse_position()
        elif self.show_next().kind == 'INTENSITE':
            self.parse_intensite()
        elif self.show_next().kind == 'DUREE':
            self.parse_duree()
        elif self.show_next().kind == 'TYPE_RAINFALL':
            self.parse_type_rainfall()
        elif self.show_next().kind == 'TYPE_CLOUD':
            self.parse_type_cloud()
        elif self.show_next().kind == 'DIRECTION':
            self.parse_direction()
        elif self.show_next().kind == 'VITESSE':
            self.parse_vitesse()
        self.indentator.dedent()
        
    def parse_move(self):
        self.indentator.indent('Parsing move')
        self.expect('MOVE')
        self.parse_coord()
        self.indentator.dedent()
