## PARSER ##
from tokens import *
from ast import Node, print_tree


class ParseError(Exception):
    pass


# recursive descent parser
class Parser:
    def __init__(self, tokens, identifiers):
        self.tokens = tokens
        self.identifiers = identifiers
        self.token_idx = 0
        self.sym = tokens[0]
        self.prev = tokens[0]
        self.node = 0


    def parse_error(self, msg):
        print(f'Parse error: {msg}')
        print(f'Current symbol: {str_of_token(self.sym)}')
        print(f'Previous symbol: {str_of_token(self.prev)}')
        print(f'Token index: {self.token_idx}')
        raise ParseError


    # Returns true while there are still tokens to scan
    def next_sym(self):
        if self.token_idx < len(self.tokens):
            self.token_idx += 1
            if self.token_idx == len(self.tokens): return False  # EOF check
            self.sym = self.tokens[self.token_idx]
            return True
        return False


    def accept(self, s):
        # s is a literal
        if s <= 0 and self.sym <= 0:
            self.prev = self.sym
            self.next_sym()
            return True
        # s is an identifier
        elif s >= 100 and self.sym > 100:
            self.prev = self.sym
            self.next_sym()
            return True
        elif self.sym == s:
            self.prev = self.sym
            self.next_sym()
            return True
        return False


    def expect(self, s):
        if self.accept(s):
            return True
        self.parse_error(f'Expected symbol {str_of_token(s)}')
        return False


    def factor(self):
        if self.accept(IDF):
            return Node(9, self.prev, [])
        elif self.accept(LIT):
            return Node(10, self.prev, [])
        elif self.accept(LPAREN):
            expr = self.expression()
            expect(RPAREN)
            return expr
        else:
            self.parse_error(f'Syntax error: ill-formed factor')
            self.next_sym()
            return None


    def expression(self):
        subexprs = []
        if self.accept(NOT):
            subexprs.append(Node(8, NOT, []))
            subexprs.append(self.factor())
            return Node(3, NONTERM, subexprs)
        else:
            # match: factor { unary-op, factor }
            fact = self.factor()
            subexprs.append(fact)
            while self.sym in {PLUS, MINUS, TIMES, DIV}:
                unary_op = Node(7, self.sym, [])
                fact_next = self.factor()
                sub_exprs.append(unary_op)
                sub_exprs.append(fact_next)
            return Node(3, NONTERM, subexprs)


    def condition(self):
        expr1 = self.expression()
        if self.sym in {EQEQ, LT, GT, LTE, GTE, NEQ}:
            cmp_op = Node(5, self.sym, [])
            self.next_sym()
        else:
            self.parse_error('Syntax error: invalid comparator')
        expr2 = self.expression()
        return Node(2, NONTERM, [expr1, cmp_op, expr2])


    def loop_step(self):
        self.accept(IDF)
        idf = self.prev
        if self.sym in {EQ, PLSEQ, MINEQ, TIMEQ, DIVEQ}:
            op = self.sym
            self.next_sym()
            expr = self.expression()
            return Node(1, NONTERM, [idf, op, expr])
        else:
            self.parse_error('Syntax error: Invalid loop increment')


    def statement(self):
        if self.accept(INT):
            idf = self.sym
            self.next_sym()
            if self.sym in {EQ, PLSEQ, MINEQ, TIMEQ, DIVEQ}:
                op = self.sym
                self.next_sym()
                expr = self.expression()
                self.expect(SEMI)
                return Node(1, NONTERM, [idf, op, expr])
            else:
                self.parse_error('Syntax error: Expected assignment operator')

        elif self.accept(IDF):
            idf = self.prev
            if self.sym in {EQ, PLSEQ, MINEQ, TIMEQ, DIVEQ}:
                op = self.sym
                self.next_sym()
                expr = self.expression()
                self.expect(SEMI)
                return Node(1, NONTERM, [idf, op, expr])
            else:
                self.parse_error('Syntax error: Expected assignment operator')

        elif self.accept(IF):
            self.expect(LPAREN)
            cond = self.condition()
            self.expect(RPAREN)
            if not self.accept(LBRACE):
                self.parse_error('Syntax error: Expected left brace {')
            bloc = self.block() # statement list
            if not self.accept(RBRACE):
                self.parse_error('Syntax error: Expected right brace }')
            return Node(1, NONTERM, [cond, bloc])

        elif self.accept(FOR):
            self.expect(LPAREN)
            stmt = self.statement()
            #self.expect(SEMI)
            cond = self.condition()
            self.expect(SEMI)
            #expr = self.statement()
            step = self.loop_step()
            self.expect(RPAREN)
            self.expect(LBRACE)
            bloc = self.block()
            self.expect(RBRACE)
            return Node(1, NONTERM, [stmt, cond, step, bloc])

        else:
            self.parse_error(f'Syntax error: ill-formed statement')


    def block(self):
        stmts = []
        while self.sym == INT or self.sym == IF or self.sym == FOR or self.sym >= 100:
            stmt = self.statement()
            stmts.append(stmt)
        return Node(0, NONTERM, stmts)


    def parse(self):
        self.node = self.block()


    def print_ast(self):
        print_tree(self.node, 0, self.identifiers)


