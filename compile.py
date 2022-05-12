import sys

from lexer import Lexer
from parser import Parser, swap_dict
from code_gen import CodeGenerator


source = sys.argv[1]
target = sys.argv[-1]
if len(sys.argv) > 3:
    flags = set(sys.argv[2:-1])
else:
    flags = set()


with open(source, 'r') as src:
    lexer = Lexer(src.read())
    tokens, identifiers = lexer.lex()
    if '-s' in flags:
        lexer.print_source()
    if '-l' in flags:
        lexer.print_info()

    parser = Parser(tokens, identifiers)
    parser.parse()
    if '-p' in flags:
        parser.print_ast()

    cgen = CodeGenerator(parser.get_ast(), swap_dict(identifiers))
    output = cgen.generate()
    if '-c' in flags:
        cgen.print_info()


with open(target, 'w') as tgt:
    tgt.write(output)

