from lexer import Lexer
from parser import Parser

with open('test.txt', 'r') as src:
    lexer = Lexer(src.read())
    tokens, identifiers = lexer.lex()
    parser = Parser(tokens, identifiers)
    parser.parse()
    parser.print_ast()

