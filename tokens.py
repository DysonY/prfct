## tokens ##
# expressions
LIT = 0
INT = 1
IDF = 100

# ctrl flow
IF = 10
FOR = 11
RET = 12

# brackets
LPAREN = 20
RPAREN = 21
LBRACE = 22
RBRACE = 23

# cmp-op
EQEQ = 30
LT = 31
GT = 32
LTE = 33
GTE = 34
NEQ = 35

# assign-op
EQ = 40
PLSEQ = 41
MINEQ = 42
TIMEQ = 43
DIVEQ = 44

# unary-op
PLUS = 50
MINUS = 51
TIMES = 52
DIV = 53

# atom-op
NOT = 60

# separator
SEMI = 70

# reserved
NONTERM = 99

## string representations of tokens ##

token_str = {
    LIT : 'LIT',
    INT : 'INT',
    IDF : 'IDF',
    IF : 'IF',
    FOR : 'FOR',
    RET : 'RET',
    LPAREN : 'LPAREN',
    RPAREN : 'RPAREN',
    LBRACE : 'LBRACE',
    RBRACE : 'RBRACE',
    EQEQ : 'EQEQ',
    LT : 'LT',
    GT : 'GT',
    LTE : 'LTE',
    GTE : 'GTE',
    NEQ : 'NEQ',
    EQ : 'EQ',
    PLSEQ : 'PLSEQ',
    MINEQ : 'MINEQ',
    TIMEQ : 'TIMEQ',
    DIVEQ : 'DIVEQ',
    PLUS : 'PLUS',
    MINUS : 'MINUS',
    TIMES : 'TIMES',
    DIV : 'DIV',
    NOT : 'NOT',
    SEMI : 'SEMI'
}


brackets = {
    '(' : LPAREN,
    ')' : RPAREN,
    '{' : LBRACE,
    '}' : RBRACE
}


op_chars = {
    '=', '<', '>', '!',
    '+', '-', '*', '/'
}


ops = {
    '=' : EQ,
    '==' : EQEQ,
    '<' : LT,
    '>' : GT,
    '<=' : LTE,
    '>=' : GTE,
    '!=' : NEQ,
    '!' : NOT,
    '+' : PLUS,
    '-' : MINUS,
    '*' : TIMES,
    '/' : DIV,
    '+=' : PLSEQ,
    '-=' : MINEQ,
    '*=' : TIMEQ,
    '/=' : DIVEQ
}


unary_ops = ['+', '-', '*', '/']
assign_ops = ['=', '+=', '-=', '*=', '/=']
cmp_ops = ['==', '<', '>', '<=', '>=', '!=']


def str_of_token(token):
    if token in token_str.keys():
        return token_str[token]
    else:
        return token


def token_of_bracket(c):
    return brackets[c]


def is_op_char(c):
    return c in op_chars


def is_op(s):
    return s in ops


def op_of_str(s):
    return ops[s]

