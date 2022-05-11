from tokens import *

# TODO issue: statement also encompasses loop_step
node_types = {
    0 : 'block',
    1 : 'statement',
    2 : 'condition',
    3 : 'expression',
    4 : 'factor',
    5 : 'cmp-op',
    6 : 'assign-op',
    7 : 'unary-op',
    8 : 'atom-op',
    9 : 'ident',
    10 : 'literal',
}


def string_of_node(node_type):
    return node_types[node_type]


# Node class for AST
class Node:
    def __init__(self, node_type, token, children):
        self.node_type = node_type # int
        self.token = token # int
        self.children = children # Node list


def print_literal(node, depth, identifiers):
    #print('  ' * depth, end='Lit: ')
    print(-1 * node.token, end=' ')


def print_ident(node, depth, identifiers):
    #print('  ' * depth, end='Idf: ')
    print(identifiers[node.token], end=' ')


def print_atom_op(node, depth, identifiers):
    assert node.node_type == 8
    #print('  ' * depth, end='Not\n')
    print('!', end='')


def print_unary_op(node, depth, identifiers):
    assert (node.token >= 50) and (node.token <= 59)
    #print('  ' * depth, end='')
    print(unary_ops[node.token - PLUS], end=' ')


def print_assign_op(node, depth, identifiers):
    assert (node.token >= 40) and (node.token <= 49)
    #print('  ' * depth, end='')
    print(assign_ops[node.token - EQ], end=' ')


def print_cmp_op(node, depth, identifiers):
    assert (node.token >= 30) and (node.token <= 39)
    print(cmp_ops[node.token - EQEQ], end=' ')


def print_factor(node, depth, identifiers):
    if node.node_type == 9:
        print_ident(node, depth + 1, identifiers)
    elif node.node_type == 10:
        print_literal(node, depth + 1, identifiers)
    else:
        print_expr(node, depth + 1, identifiers)


def print_expr(node, depth, identifiers):
    print('Expr: ')
    for child in node.children:
        print_tree(child, depth + 1, identifiers)
    print()


def print_cond(node, depth, identifiers):
    print('Cond: ')
    print_expr(node.children[0], depth + 1, identifiers)
    print_cmp_op(node.children[1], depth + 1, identifiers)
    print_expr(node.children[2], depth + 1, identifiers)
    print()


def print_stmt(node, depth, identifiers):
    print('Stmt: ')
    for child in node.children:
        print_tree(child, depth + 1, identifiers)
    print()


def print_block(node, depth, identifiers):
    print('Block: ')
    for child in node.children:
        print_stmt(child, depth + 1, identifiers)
    print()


print_fns = [
    print_block,
    print_stmt,
    print_cond,
    print_expr,
    print_factor,
    print_cmp_op,
    print_assign_op,
    print_unary_op,
    print_atom_op,
    print_ident,
    print_literal
]


def print_tree(root, depth, identifiers):
    idx = root.node_type
    print_fns[idx](root, depth, identifiers)

