import re
import sys
from token1 import Token

regexExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'in\b', 'IN'),
    (r'at\b', 'AT'),
    (r'map\b', 'MAP'),
    (r'wind\b', 'WIND'),
    (r'sun\b', 'SUN'),
    (r'cloud\b', 'CLOUD'),
    (r'rainfall\b', 'RAINFALL'),
    (r'forecast\%', 'MAIN'),
    (r'\%forecast', 'ENDMAIN'),
    (r'vitesse\b', 'VITESSE'),
    (r'direction\b', 'DIRECTION'),
    (r'position\b', 'POSITION'),
    (r'duree\b', 'DUREE'),
    (r'indiceUV\b', 'UV'),
    (r'type_rainfall\b', 'TYPE_RAIN'),
    (r'type_cloud\b', 'TYPE_CLOUD'),
    (r'intensite\b', 'INTENSITE'),
    (r'pluie\b', 'PLUIE'),
    (r'neige\b', 'NEIGE'),
    (r'cumulonimbus\b', 'CUMULONIMBUS'),
    (r'cirrus\b', 'CIRRUS'),
    (r'cumulus\b', 'CUMULUS'),
    (r'faible\b', 'FAIBLE'),
    (r'forte\b', 'FORTE'),
    (r'normale\b', 'NORMALE'),
    (r'\/\*', 'LCOMMENT'),
    (r'\*\/', 'RCOMMENT'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'\[', 'LBRACKET'),
    (r'\]', 'RBRACKET'),
    (r'\;', 'SEMICOLON'),
    (r'\:', 'COLON'),
    (r'\,', 'COMMA'),
    (r'\/\/', 'DBAR'),
    (r'\|', 'BAR'),
    (r'\.', 'DOT'),
    (r'\=', 'ASSIGN'),
    (r'\-\>', 'MOVE'),
    (r'\-', 'SUB'),
    (r'\*', 'DEL'),
    (r'\<', 'WEST'),
    (r'\>', 'EAST'),
    (r'\^', 'NORTH'),
    (r'V', 'SOUTH'),
    (r'\d+\.\d+', 'LATLONG'),
    (r'\d+', 'INT'),
    (r'[a-z0-9_]+', 'IDENTIFIER'),
    (r'[a-zA-Z]\w*', 'IDENTIFIERCOMMENT')
]


class Lexer:

    def __init__(self):
        self.tokens = []

    def lex(self, inputText):

        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                        break
                if not match:
                    print("No match - L:{}, C:{}".format(lineNumber, position))
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("lexer: analysis successful!")
        return self.tokens


def main():
    inputText = open("./test0.met").readlines()
    myLex = Lexer()
    for token in (myLex.lex(inputText)):
        print (token)
    


if __name__ == '__main__':
    main()


