## CODE GENERATION ##
from tokens import *
from ast import Node, print_tree

# Identifier aliases begin with _idf
# Literal aliases begin with _lit
# TODO merge assign_fns, cmp_fns, unary_fns into a single op_fns dictionary


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
        self.reserved_fns = { '_add', '_sub', '_mul', '_div' }

        self.assign_fns = {
            EQ : '_copy',
            PLSEQ : '_copyadd',
            MINEQ : '_copysub',
            TIMEQ : '_copymul',
            DIVEQ : '_copydiv'
        }

        self.cmp_fns = {
            EQEQ : '_eq',
            LT : '_lt',
            GT : '_gt',
            LTE : '_lte',
            GTE : '_gte',
            NEQ : '_neq'
        }

        self.unary_fns = {
            PLUS : '_add',
            MINUS : '_sub',
            TIMES : '_mul',
            DIV : '_div'
        }


    # Reserve a function handle
    def reserve(self, s):
        self.reserved_fns.add(s)


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


    def reserve_literals(self):
        temp_lines = []
        for (val, lit) in self.lit_aliases.items():
            temp_lines.append(f'def {lit}():')
            temp_lines.append(f'    _temp = 0')
            for i in range(val):
                temp_lines.append(f'    _temp += 1')
            temp_lines.append(f'    return temp')
        temp_lines.append('\n')
        return '\n'.join(temp_lines)


    def is_literal(self, node):
        return node.node_type == 10


    def is_ident(self, node):
        return node.node_type == 9


    def gen_expr(self, node):
        # Leaf node check
        if len(node.children) == 0:
            if self.is_literal(node):
                return self.lit_aliases[node.token] + '()'
            elif self.is_ident(node):
                return self.idf_aliases[node.token]

        # Determine type of expression based on first child node
        first = node.children[0]
        if self.is_literal(first):
            return self.lit_aliases[first.token] + '()'
        elif self.is_ident(first):
            return self.idf_aliases[first.token]
        elif first.node_type == 8: # atom-op check
            fact = self.gen_expr(node.children[1])
            self.reserve('_not')
            return '_not({fact})'
        else:
            # TODO account for multiple unary ops
            #return '(ARITH EXPRESSION)'
            factors = []
            subexpr_idx = 1
            fact = self.gen_expr(first)

            # Enforce left-branching order
            while subexpr_idx < len(node.children):
                unary_fn = self.unary_fns[node.children[subexpr_idx].token]
                subexpr_idx += 1
                factors.append(unary_fn)
                factors.append('(')
                factors.append(fact)
                factors.append(', ')

                fact = self.gen_expr(node.children[subexpr_idx])
                factors.append(next_fact)
                subexpr_idx += 1

            # Add right parentheses
            rparen_count = 0
            for f in factors:
                if f == '(':
                    rparen_count += 1

            return ''.join(factors) + (')' * rparen_count)


    def gen_cond(self, node, depth):
        expr1 = node.children[0]
        op = node.children[1]
        expr2 = node.children[2]

        cond_var = self.next_local()
        local1 = self.next_local()
        local2 = self.next_local()

        expr_str1 = self.gen_expr(expr1)
        expr_str2 = self.gen_expr(expr2)

        self.add_line(('  ') * depth + f'{local1} = {expr_str1}')
        self.add_line(('  ') * depth + f'{local2} = {expr_str2}')

        cmp_fn = self.cmp_fns[op.token]
        self.reserve(cmp_fn)
        self.add_line(('  ') * depth + f'{cond_var} = {cmp_fn}({local1}, {local2})')
        return cond_var


    def gen_ifstmt(self, node, depth):
        cond_var = self.gen_cond(node.children[0], depth) 
        #self.add_line(('\t' * depth) + cond_str)
        #cond_var = self.next_local()
        check_var = self.next_local()
        self.add_line(('  ' * depth) + f'for {check_var} in range({cond_var}):')
        self.gen_block(node.children[1], depth + 1)


    def gen_asgstmt(self, node, depth):
        idf = node.children[0]
        op = node.children[1]
        expr = node.children[2].children[0]
        idf_alias = self.idf_aliases[idf.token]
        op_fn = self.assign_fns[op.token]
        self.reserve(op_fn)
        if self.is_literal(expr):
            lit_fn = self.lit_aliases[expr.token]
            self.add_line(('  ' * depth) +
                            f'{idf_alias} = {op_fn}({idf_alias}, {lit_fn}())')
        else:
            expr_str = self.gen_expr(expr)
            self.add_line(('  ' * depth) +
                            f'{idf_alias} = {op_fn}({idf_alias}, {expr_str})')


    def gen_forstmt(self, node, depth):
        # Alg for compiling a for statement:
        # - From FOR node, get start/stop/step
        # - Compute input to range function: floor((stop - start) / step)
        # - At start of loop, recover true idx: idf = start <op> (i * step)
        # - Compile block w/ additional indent

        asg = node.children[0]
        cond = node.children[1]
        incr = node.children[2]
        op_fn = self.assign_fns[incr.children[1].token]
        block = node.children[3]

        loop_idx = self.next_local()
        true_idx = self.idf_aliases[incr.children[0].token]
        start = self.gen_expr(asg.children[2])
        stop = self.gen_expr(cond.children[2])
        step = self.gen_expr(incr.children[2])

        range_arg = self.next_local()
        set_range = f'{range_arg} = _div(_sub({stop}, {start}), {step})'
        self.add_line(('  ' * depth) + set_range)

        for_str = f'for {loop_idx} in range({range_arg}):'
        self.add_line(('  ' * depth) + for_str)
        recover_idx_str = f'{true_idx} = {op_fn}({start}, _mul({loop_idx}, {step}))'
        self.add_line(('  ' * (depth + 2)) + recover_idx_str)

        self.gen_block(block, depth + 1)
        self.reserve(op_fn)


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

        main_code = '\n'.join(self.lines)
        reserved_lit_code = self.reserve_literals()

        full_code = [reserved_lit_code, main_code]
        return '\n'.join(full_code)


    def print_info(self):
        print('\n===== CODE GEN LOGGING =====')
        print('Literal aliases:', self.lit_aliases)
        print('Identifier aliases:', self.idf_aliases)
        print('Reserved functions:', self.reserved_fns)
        print('Output:')
        print('\n'.join(self.lines))

