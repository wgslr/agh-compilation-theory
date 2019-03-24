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

def p_start(p):
    """start : expression
             | start expression"""
    # if len(p) == 2:
    #     print("p[1]=", p[1])
    # else:
    #     print("p[2]=", p[2])
    p[0] = p[1]


def p_expr(p):
    """expression : assignment
                  | assignment ';'
                  | cond
                  | operation ';'"""  # fixme remove operation, cond(Added only for tests purpose)
    p[0] = p[1]


def p_cond(p):
    """cond : cmp
            | operation"""
    p[0] = p[1]


def p_operation(p):
    """operation : num
                 | neg_num
                 | transpose"""
    p[0] = p[1]


# -------------------------
# Assignments
# -------------------------

def p_assignment(p):
    """assignment : ID '=' cond"""
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
