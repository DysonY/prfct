# TODO line_idx is not updated correctly on blank lines
# TODO lex integer literals as their negation
# negative number handling?

from tokens import *


def is_space(c):
    return c == '\t' or c == ' '


def is_newline(c):
    return c == '\n'


def is_whitespace(c):
    return is_space(c) or is_newline(c)


def is_ident_start(c):
    return c.isalpha() or c == '_'


def is_numeric(c):
    return c.isdigit()


def is_ident(c):
    return is_ident_start(c) or is_numeric(c)


def is_bracket(c):
    return c in ['(', ')', '{', '}']


def is_semi(c):
    return c == ';'


class Lexer:
    def __init__(self, code_str):
        self.code_str = code_str
        self.line_idx = 0
        self.char_idx = 0
        self.next_idf = 100
        self.identifiers = dict()
        self.eof_reached = False
        self.reserved = {
            'if' : IF, 
            'for' : FOR,
            'int' : INT,
            'return' : RET
        }
        self.tokens = []


    def lex_error(self, msg):
        print(f"Lexing error on line {self.line_idx}")
        print(msg)


    def lookahead(self):
        if self.char_idx >= len(self.code_str):
            return ''
        return self.code_str[self.char_idx + 1]


    def check_eof(self):
        if self.char_idx >= len(self.code_str):
            self.eof_reached = True


    def burn_wspace(self):
        while is_whitespace(self.code_str[self.char_idx]):
            if is_newline(self.code_str[self.char_idx]):
                self.line_idx += 1
            self.char_idx += 1
            self.check_eof()
            if self.eof_reached:
                return


    def is_reserved(self, idf):
        return idf in self.reserved.keys()


    def match_ident(self):
        ident = []
        while is_ident(self.code_str[self.char_idx]):
            ident.append(self.code_str[self.char_idx])
            self.char_idx += 1
            self.check_eof()
            if self.eof_reached:
                return
            #print(self.char_idx, self.code_str[self.char_idx])
        idf = ''.join(ident)
        if self.is_reserved(idf):
            self.tokens.append(self.reserved[idf])
        else:
            if idf not in self.identifiers.keys():
                self.identifiers[idf] = self.next_idf
                self.next_idf += 1
            self.tokens.append(self.identifiers[idf])


    def match_bracket(self):
        br_token = token_of_bracket(self.code_str[self.char_idx])
        self.tokens.append(br_token)


    def match_op(self):
        s = self.code_str[self.char_idx]
        c_next = self.lookahead()
        if is_op_char(c_next):
            s += c_next
            self.char_idx += 1
        if is_op(s):
            self.tokens.append(op_of_str(s))
        else:
            print(s)
            self.lex_error('-> Invalid operator')


    def match_semi(self):
        self.tokens.append(SEMI)


    def match_literal(self):
        digits = []
        while(is_numeric(self.code_str[self.char_idx])):
            digits.append(self.code_str[self.char_idx])
            self.char_idx += 1
            self.check_eof()
            if self.eof_reached:
                break
            if is_ident_start(self.code_str[self.char_idx]):
                print(self.code_str[self.char_idx])
                self.lex_error('-> Invalid literal')
        lit = int(''.join(digits)) * -1
        self.tokens.append(lit)


    def lex(self):
        while self.char_idx < len(self.code_str):
            self.burn_wspace()
            self.check_eof()
            if self.eof_reached:
                break
            if is_ident_start(self.code_str[self.char_idx]):
                self.match_ident()
            elif is_bracket(self.code_str[self.char_idx]):
                #print(self.char_idx, self.code_str[self.char_idx])
                self.match_bracket()
                self.char_idx += 1
            elif is_op_char(self.code_str[self.char_idx]):
                self.match_op()
                self.char_idx += 1
            elif is_semi(self.code_str[self.char_idx]):
                self.match_semi()
                self.char_idx += 1
            elif is_numeric(self.code_str[self.char_idx]):
                self.match_literal()
            else:
                self.char_idx += 1
        self.print_info()
        return self.tokens, self.identifiers


    def print_info(self):
        print('===== SOURCE CODE =====')
        print(self.code_str)
        print('===== LEXICAL ANALYSIS =====')
        print('Lines:', self.line_idx)
        print('Identifiers:', self.identifiers)
        print('Tokens: ', end='')
        token_strs = []
        for t in self.tokens:
            if t in self.identifiers.values():
                token_strs.append('IDF')
            else:
                token_strs.append(str_of_token(t))
        print(token_strs, end='\n\n')


#with open('test.txt', 'r') as src:
#    lexer = Lexer(src.read())
#    lexer.lex()

