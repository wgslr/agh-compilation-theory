#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens
literals = scanner.literals

symtab = {}

precedence = (
    ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("left", '<', '>', 'EQ', 'NEQ', 'GEQ', 'LEQ'),
    ("left", '+', '-'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", '*', '/'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('right', '\''),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                  scanner.find_column(p.lexer.lexdata,
                                                                                                      p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


# -------------------------
# Main productions
# -------------------------

def p_mul_expressions(p):
    """mul_expressions : expression
                       | expression mul_expressions"""
    # if len(p) == 2:
    #     print("p[1]=", p[1])
    # else:
    #     print("p[2]=", p[2])
    p[0] = p[1]


def p_expr(_p):
    """expression : block
                  | base_expr
                  | base_expr ';'
                  | if_statement
                  | loop"""


def p_base_expr(_p):
    """base_expr : assignment
                 | return
                 | print"""


def p_cond(p):
    """cond : cmp
            | operation"""
    p[0] = p[1]


def p_operation(p):
    """operation : num
                 | neg_num
                 | transpose"""
    p[0] = p[1]


def p_block(p):
    """block : '{' mul_expressions '}'"""
    p[0] = p[2]


def p_print(_p):
    """print : PRINT print_body"""


def p_print_body(_p):
    """print_body : STRING
                  | cond
                  | print_body ',' cond"""


def p_return(_p):
    """return : RETURN cond
              | RETURN"""


# -------------------------
# Loops
# -------------------------

def p_loop(_p):
    """loop : while
            | for"""


def p_while(_p):
    """while : WHILE '(' cond ')' loop_body"""


def p_for(_p):
    """for : FOR var '=' int_num_var ':' int_num_var loop_body"""


def p_loop_body(_p):
    """loop_body : loop_expr
                 | loop_expr ';'
                 | '{' mul_loop_expr '}'"""


def p_loop_expr(_p):
    """loop_expr : base_expr
                 | loop
                 | if_loop_statement
                 | BREAK
                 | CONTINUE"""


def p_mul_loop_expr(_p):
    """mul_loop_expr : mul_loop_expr loop_body
                     | loop_body"""


# -------------------------
# If statements
# -------------------------

def p_if_statement(_p):
    """if_statement : IF '(' cond ')' expression else_statement"""


def p_else_statement(_p):
    """else_statement : ELSE expression
                      | empty"""


def p_if_loop_statement(_p):
    """if_loop_statement : IF '(' cond ')' loop_body else_loop_statement"""


def p_else_loop_statement(_p):
    """else_loop_statement : ELSE loop_body
                      | empty"""


def p_empty(_p):
    """empty : """


# -------------------------
# Assignments
# -------------------------

def p_assignment(p):
    """assignment : ID '=' cond
                  | ID '=' STRING"""
    symtab[p[1]] = p[3]
    p[0] = p[3]


def p_addassignment(p):
    """assignment : ID ADDASSIGN cond"""
    symtab[p[1]] += p[3]
    p[0] = symtab[p[1]]


def p_subassignment(p):
    """assignment : ID SUBASSIGN cond"""
    symtab[p[1]] -= p[3]
    p[0] = symtab[p[1]]


def p_mulassignment(p):
    """assignment : ID MULASSIGN cond"""
    symtab[p[1]] *= p[3]
    p[0] = symtab[p[1]]


def p_divassignment(p):
    """assignment : ID DIVASSIGN cond"""
    symtab[p[1]] /= p[3]
    p[0] = symtab[p[1]]


# -------------------------
# Numeric and variables
# -------------------------

def p_var(p):
    """var : ID"""
    val = symtab.get(p[1])
    if val:
        p[0] = val
    else:
        p[0] = 1


def p_num(p):
    """num : INTNUM 
           | FLOATNUM
           | var"""
    p[0] = p[1]


def p_int_num_var(p):
    """int_num_var : INTNUM
                   | var"""
    p[0] = p[1]


# -------------------------
# Unary operations
# -------------------------

def p_neg(p):
    """neg_num : '-' num %prec UMINUS"""
    p[0] = -p[2]


def p_transpose(p):
    """transpose : ID '\\'' """
    p[0] = p[1]


# -------------------------
# Binary operations
# -------------------------

def p_operation_sum(p):
    """operation : operation '+' operation
                 | operation '-' operation"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]


def p_operation_dot_sum(p):
    """operation : operation DOTADD operation
                 | operation DOTSUB operation"""
    if p[2] == '.+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]


def p_operation_mul(p):
    """operation : operation '*' operation
                 | operation '/' operation"""
    if p[2] == '*':
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1] / p[3]


def p_operation_dot_mul(p):
    """operation : operation DOTMUL operation
                 | operation DOTDIV operation"""
    if p[2] == '.*':
        p[0] = p[1] * p[3]
    else:
        p[0] = p[1] / p[3]


# -------------------------
# Binary comparisons operations
# -------------------------

def p_operation_cmp(p):
    """cmp : operation '<' operation
           | operation '>' operation"""
    if p[2] == '<':
        p[0] = p[1] < p[3]
    else:
        p[0] = p[1] > p[3]


def p_operation_cmp_eq(p):
    """cmp : operation EQ operation
           | operation NEQ operation"""
    if p[2] == '==':
        p[0] = p[1] == p[3]
    else:
        p[0] = p[1] != p[3]


def p_operation_cmp_geq(p):
    """cmp : operation GEQ operation
           | operation LEQ operation"""
    if p[2] == '>=':
        p[0] = p[1] >= p[3]
    else:
        p[0] = p[1] <= p[3]


def p_operation_group(p):
    """operation : '(' operation ')'"""
    p[0] = p[2]


parser = yacc.yacc()
