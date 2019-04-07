#!/usr/bin/python

from __future__ import print_function
import scanner
import ply.yacc as yacc

import AST

tokens = scanner.tokens
literals = scanner.literals


precedence = (
    ('nonassoc', 'IF'),
    ('nonassoc', 'ELSE'),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('nonassoc', '<', '>', 'EQ', 'NEQ', 'GEQ', 'LEQ'),
    ('left', '+', '-'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('right', '\''),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
              .format(p.lineno, scanner.find_column(p.lexer.lexdata, p),
                      p.type, p.value))
    else:
        print("Unexpected end of input")


# -------------------------
# Main productions
# -------------------------

def p_instructions(p):
    """instructions : instruction
                    | instruction instructions"""
    if len(p) == 2:
        p[0] = AST.Instructions([p[1]])
    else:
        p[0] = p[2]
        p[0].nodes = [p[1]] + p[0].nodes


def p_instruction(p):
    """instruction : block
                   | conditional
                   | loop
                   | statement ';'
                   | error ';'"""
    p[0] = p[1]


def p_statement(p):
    """statement : assignment
                 | return
                 | print
                 | BREAK
                 | CONTINUE"""
    p[0] = p[1]


def p_expression(p):
    """expression : comparison_expression
                  | numeric_expression"""
    p[0] = p[1]


def p_block(p):
    """block : '{' instructions '}'
             | '{' error '}'"""
    p[0] = p[2]


def p_print(p):
    """print : PRINT print_body"""
    p[0] = AST.Print(p[2])


def p_print_body(p):
    """print_body : string
                  | expression
                  | string ',' print_body
                  | expression ',' print_body"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[3]
        p[0] = [p[1]] + p[0]


def p_return(p):
    """return : RETURN expression
              | RETURN"""
    if len(p) == 2:
        p[0] = AST.Return()
    else:
        p[0] = AST.Return(p[2])


def p_string(p):
    """string : STRING"""
    p[0] = AST.String(p[1])

# -------------------------
# Matrices
# -------------------------


def p_vector(p):
    """vector : '[' vector_body ']'
              | '[' ']'"""
    if len(p) == 3:
        p[0] = AST.Vector([])
    else:
        p[0] = AST.Vector(p[2])
        


def p_vector_body(p):
    """vector_body : numeric_expression
                   | vector_body ',' numeric_expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0] += [p[3]]


def p_matrix(p):
    """matrix : '[' matrix_body ']'
              | '[' ']'"""
    if len(p) == 3:
        p[0] = AST.Vector([])
    else:
        p[0] = AST.Vector(p[2])


def p_matrix_body(p):
    """matrix_body : vector
                   | matrix_body ',' vector"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0] += [p[3]]


# -------------------------
# Arrays
# -------------------------

def p_array_range(p):
    """array_range : ID '[' expression ',' expression ']'"""
    p[0] = AST.Reference(AST.Variable(p[1]), [p[3], p[5]])


# -------------------------
# Funs
# -------------------------

def p_fun(p):
    """fun : fun_name '(' numeric_expression ')'
           | fun_name '(' error ')'"""
    p[0] = AST.FunctionCall(p[1], p[3])


def p_fun_name(p):
    """fun_name : ZEROS
                | ONES
                | EYE"""
    p[0] = p[1]


# -------------------------
# Loops
# -------------------------

def p_loop(p):
    """loop : while
            | for"""
    p[0] = p[1]


def p_while(p):
    """while : WHILE '(' expression ')' instruction"""
    p[0] = AST.While(p[3], p[5])


def p_for(p):
    """for : FOR ID '=' numeric_expression ':' numeric_expression instruction"""
    p[0] = AST.For(AST.Variable(p[2]), p[4], p[6], p[7])


# -------------------------
# If statements
# -------------------------

def p_conditional(p):
    """conditional : IF '(' expression ')' instruction %prec IF
                   | IF '(' expression ')' instruction ELSE instruction"""
    if len(p) == 6:
        else_body = None
    else:
        else_body = p[7]
    p[0] = AST.If(p[3], p[5], else_body)


# -------------------------
# Assignments
# -------------------------

def p_assignment_lhs(p):
    """assignment_lhs : var
                      | array_range"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : assignment_lhs assignment_operator expression
                  | assignment_lhs '=' string"""
    p[0] = AST.Assignment(p[2], p[1], p[3])
    


def p_assignment_operator(p):
    """assignment_operator : '='
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""
    p[0] = p[1]


# -------------------------
# Numerics and variables
# -------------------------

def p_var(p):
    """var : ID
           | var '[' numeric_expression ']'"""
    if len(p) == 2:
        p[0] = AST.Variable(p[1])
    else:
        # TODO
        pass


def p_num(p):
    """num : INTNUM
           | FLOATNUM
           | var"""
    if isinstance(p[1], (int, long)):
        p[0] = AST.IntNum(p[1])
    elif isinstance(p[1], float):
        p[0] = AST.FloatNum(p[1])
    else:
        p[0] = p[1]


# -------------------------
# Numeric expressions
# -------------------------

def p_unary_op(p):
    """unary_op : negation
                | transposition"""
    p[0] = p[1]


def p_neg(p):
    """negation : '-' numeric_expression %prec UMINUS"""
    p[0] = AST.UnaryExpr('NEGATE', p[2])


def p_transposition(p):
    r"""transposition : numeric_expression '\''"""
    p[0] = AST.UnaryExpr('TRANSPOSE', p[1])


def p_numeric_expression(p):
    """numeric_expression : num
                          | matrix
                          | unary_op
                          | fun
                          | '(' numeric_expression ')'"""
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_bin_numeric_expression(p):
    """numeric_expression : numeric_expression '+' numeric_expression
                          | numeric_expression '-' numeric_expression
                          | numeric_expression '*' numeric_expression
                          | numeric_expression '/' numeric_expression
                          | numeric_expression DOTADD numeric_expression
                          | numeric_expression DOTSUB numeric_expression
                          | numeric_expression DOTMUL numeric_expression
                          | numeric_expression DOTDIV numeric_expression"""
    p[0] = AST.ArithmeticOperation(p[2], p[1], p[3])


# -------------------------
# Binary comparisons expressions
# -------------------------

def p_comparison_expression(p):
    """comparison_expression : numeric_expression '<' numeric_expression
           | numeric_expression '>' numeric_expression
           | numeric_expression EQ numeric_expression
           | numeric_expression NEQ numeric_expression
           | numeric_expression GEQ numeric_expression
           | numeric_expression LEQ numeric_expression
           | '(' comparison_expression ')'"""
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = AST.Comparison(p[2], p[1], p[3])


# TODO Fix "Lexer instance has no attribute 'find_column'"
scanner = scanner.lexer
parser = yacc.yacc()
