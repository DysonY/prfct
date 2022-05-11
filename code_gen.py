## CODE GENERATION ##
from tokens import *
from ast import Node, print_tree

# Identifier aliases begin with _idf
# Literal aliases begin with _lit


# 0 -> a, 1 -> b, 2 -> c, etc.
def str_of_num(num):
    chars = []
    for digit in str(num):
        chars.append(chr(ord(digit) + 49))
    return ''.join(chars)


class CodeGenerator:
    def __init__(self, root, identifiers):
        self.root = root  #  Node (block)
        self.identifiers = identifiers
        self.idf_aliases = dict()  # { str : str }
        self.lit_aliases = dict()  # { int : str }
        self.curr_local = 0
        self.lines = ['def main():']

        self.assign_fns = {
            EQ : '_copy',
            PLSEQ : '_copyadd',
            MINEQ : '_copysub',
            TIMEQ : '_copymul',
            DIVEQ : '_copydiv'
        }


    def add_line(self, line):
        self.lines.append(line)


    def alias_of_idf(self, idf):
        return '_idf' + self.identifiers[idf]


    def alias_of_lit(self, lit):
        return '_lit' + str_of_num(lit)


    def next_local(self):
        local = '_loc' + str_of_num(self.curr_local)
        self.curr_local += 1
        return local


    # 1st traversal; generate aliases for all literals and identifiers
    def collect_aliases(self, node):
        if node.node_type == 10:
            self.lit_aliases[node.token] = self.alias_of_lit(node.token)
            return
        elif node.node_type == 9:
            self.idf_aliases[node.token] = self.alias_of_idf(node.token)
            return
        elif len(node.children) == 0: return
        for child in node.children:
            self.collect_aliases(child)


    def is_literal(self, node):
        return node.node_type == 10


    def gen_expr(self, node):
        return '(expr)'


    def gen_cond(self, node, depth):
        # TODO
        pass


    def gen_ifstmt(self, node, depth):
        self.gen_cond(node.children[0], depth)
        #self.add_line(('\t' * depth) + cond_str)
        cond_var = self.next_local()
        check_var = self.next_local()
        self.add_line(('  ' * depth) + f'for {check_var} in range({cond_var}):')
        self.gen_block(node.children[1], depth + 1)


    def gen_asgstmt(self, node, depth):
        idf = node.children[0]
        op = node.children[1]
        expr = node.children[2]
        if self.is_literal(expr.children[0]):
            idf_alias = self.idf_aliases[idf.token]
            op_fn = self.assign_fns[op.token]
            lit_fn = self.lit_aliases[expr.token]
            self.add_line(('  ' * depth) +
                            f'{idf_alias} = {op_fn}({idf_alias}, {lit_fn}())')
        else:
            # TODO copy expr to lit
            pass


    def gen_forstmt(self, node, depth):
        asg = node.children[0]
        cond = node.children[1]
        incr = node.children[2]
        op = incr.children[1].token
        block = node.children[3]

        loop_idx = self.next_local()
        start = self.gen_expr(asg.children[2])
        stop = self.gen_expr(cond.children[2])
        step = self.gen_expr(incr.children[2])

        # ...
        self.gen_block()


    def gen_stmt(self, node, depth):
        if len(node.children) == 2:
            self.gen_ifstmt(node, depth)
        elif len(node.children) == 3:
            self.gen_asgstmt(node, depth)
        elif len(node.children) == 4:
            self.gen_forstmt(node, depth)
        else:
            # TODO raise genError
            print('Invalid number of sub-expressions in statment')


    def gen_block(self, node, depth):
        for child in node.children:
            self.gen_stmt(child, depth + 1)


    def generate(self):
        self.collect_aliases(self.root)
        self.gen_block(self.root, 1)
        self.print_info()


    def print_info(self):
        print('\n===== CODE GEN LOGGING =====')
        print('Literal aliases:', self.lit_aliases)
        print('Identifier aliases:', self.idf_aliases)
        print('Output:')
        print('\n'.join(self.lines))

