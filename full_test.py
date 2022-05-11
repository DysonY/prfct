from lexer import Lexer
from parser import Parser, swap_dict
from code_gen import CodeGenerator

with open('test.txt', 'r') as src:
    lexer = Lexer(src.read())
    tokens, identifiers = lexer.lex()
    parser = Parser(tokens, identifiers)
    parser.parse()
    parser.print_ast()
    cgen = CodeGenerator(parser.get_ast(), swap_dict(identifiers))
    cgen.generate()

