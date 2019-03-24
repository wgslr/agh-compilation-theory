#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens
literals = scanner.literals

symtab = {}

precedence = (
    ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
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
                  | operation
                  | operation ';'"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : ID '=' operation"""
    symtab[p[1]] = p[3]
    p[0] = p[3]


def p_addassignment(p):
    """assignment : ID ADDASSIGN operation"""
    symtab[p[1]] += p[3]
    p[0] = symtab[p[1]]


def p_subassignment(p):
    """assignment : ID SUBASSIGN operation"""
    symtab[p[1]] -= p[3]
    p[0] = symtab[p[1]]


def p_mulassignment(p):
    """assignment : ID MULASSIGN operation"""
    symtab[p[1]] *= p[3]
    p[0] = symtab[p[1]]


def p_divassignment(p):
    """assignment : ID DIVASSIGN operation"""
    symtab[p[1]] /= p[3]
    p[0] = symtab[p[1]]


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


def p_neg(p):
    """neg_num : '-' num %prec UMINUS"""
    p[0] = -p[2]


def p_transpose(p):
    """transpose : ID '\\'' """
    p[0] = p[1]


def p_operation(p):
    """operation : num
                 | neg_num
                 | transpose"""
    p[0] = p[1]


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


def p_operation_group(p):
    """operation : '(' operation ')'"""
    p[0] = p[2]


parser = yacc.yacc()
