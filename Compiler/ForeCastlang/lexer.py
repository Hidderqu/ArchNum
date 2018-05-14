import re
import sys
from token import Token

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
    (r'forecast\%\b', 'MAIN'),
    (r'vitesse\b', 'VITESSE'),
    (r'direction\b', 'DIRECTION'),
    (r'position\b', 'POSITION'),
    (r'duree\b', 'DUREE'),
    (r'indiceUV\b', 'UV'),
    (r'type\b', 'TYPE'),
    (r'intensite\b', 'INTENSITE'),
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
    (r'\/\/', 'SEPARATOR'),
    (r'\|', 'BAR'),
    (r'\.', 'DOT'),
    (r'\=', 'ASSIGN'),
    (r'\-', 'SUB'),
    (r'\*', 'DEL'),
    (r'\<', 'WEST'),
    (r'\>', 'EAST'),
    (r'\^', 'NORTH'),
    (r'\V', 'SOUTH'),
    (r'\-\>', 'MOVE'),
    (r'[a-z0-9_]+', 'IDENTIFIER'),
    (r'\d+\.\d+', 'LONGLAT'),
    (r'\d+', 'POS'),
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
                    print(inputText[position])
                    print("no match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("lexer: analysis successful!")
        return self.tokens


def main():
    inputText = open("../Test/add.c").readlines()
    myLex = Lexer()
    for token in (myLex.lex(inputText)):
        print (token)
    


if __name__ == '__main__':
    main()


