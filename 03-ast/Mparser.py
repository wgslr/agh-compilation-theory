#!/usr/bin/python

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

def p_many_expressions(p):
    """many_expressions : expression
                       | expression many_expressions"""


def p_expr(p):
    """expression : block
                  | base_expr
                  | if_statement
                  | loop"""


def p_base_expr(p):
    """base_expr : assignment ';'
                 | return ';'
                 | print ';'"""


def p_cond(p):
    """cond : cmp
            | operation"""
    p[0] = p[1]


def p_operation(p):
    """operation : num
                 | unary_op
                 | fun"""
    p[0] = p[1]


def p_block(p):
    """block : '{' many_expressions '}'"""


def p_print(p):
    """print : PRINT print_body"""


def p_print_body(p):
    """print_body : STRING
                  | cond
                  | print_body ',' cond"""


def p_return(p):
    """return : RETURN cond
              | RETURN """


# -------------------------
# Matrices
# -------------------------

def p_vector(p):
    """vector : '[' vector_body ']'"""


def p_vector_body(p):
    """vector_body : num
                   | vector_body ',' num
                   | empty"""


def p_matrix(p):
    """matrix : '[' matrix_body ']'"""


def p_matrix_body(p):
    """matrix_body : vector
                   | matrix_body ',' vector
                   | empty"""


# -------------------------
# Arrays
# -------------------------

def p_array_range(p):
    """array_range : ID '[' int_num_var ',' int_num_var ']'"""


# -------------------------
# Funs
# -------------------------

def p_fun(p):
    """fun : fun_name '(' num ')'"""


def p_fun_name(p):
    """fun_name : ZEROS
                | ONES
                | EYE"""


# -------------------------
# Loops
# -------------------------

def p_loop(p):
    """loop : while
            | for"""


def p_while(p):
    """while : WHILE '(' cond ')' loop_body"""


def p_for(p):
    """for : FOR var '=' int_num_var ':' int_num_var loop_body"""


def p_loop_body(p):
    """loop_body : loop_expr
                 | '{' many_loop_expr '}'"""


def p_loop_expr(p):
    """loop_expr : base_expr
                 | loop
                 | if_loop_statement
                 | BREAK ';'
                 | CONTINUE ';'"""


def p_many_loop_expr(p):
    """many_loop_expr : many_loop_expr loop_expr
                     | loop_expr"""


# -------------------------
# If statements
# -------------------------

def p_if_statement(p):
    """if_statement : IF '(' cond ')' expression %prec IF
                    | IF '(' cond ')' expression ELSE expression"""


def p_if_loop_statement(p):
    """if_loop_statement : IF '(' cond ')' loop_body %prec IF
       if_loop_statement : IF '(' cond ')' loop_body ELSE loop_body"""


def p_empty(p):
    """empty : """


# -------------------------
# Assignments
# -------------------------

def p_assignee(p):
    """assignee : ID
                | array_range"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : assignee '=' cond
                  | assignee '=' matrix
                  | assignee '=' STRING"""
    p[0] = AST.Assignment(p[2], p[1], p[3])


def p_opassignment(p):
    """assignment : assignee ADDASSIGN cond
                  | assignee SUBASSIGN cond
                  | assignee MULASSIGN cond
                  | ID DIVASSIGN cond"""
    p[0] = AST.Assignment(p[2], p[1], p[3])


# -------------------------
# Numeric and variables
# -------------------------

def p_var(p):
    """var : ID"""
    p[0] = AST.Variable()


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

def p_unary_op(p):
    """unary_op : neg_num
                | transpose"""


def p_neg(p):
    """neg_num : '-' num %prec UMINUS"""


def p_transpose(p):
    """transpose : operation '\\'' """


# -------------------------
# Binary operations
# -------------------------

def p_operation_sum(p):
    """operation : operation '+' operation
                 | operation '-' operation"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_operation_dot_sum(p):
    """operation : operation DOTADD operation
                 | operation DOTSUB operation"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_operation_mul(p):
    """operation : operation '*' operation
                 | operation '/' operation"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_operation_dot_mul(p):
    """operation : operation DOTMUL operation
                 | operation DOTDIV operation"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])


# -------------------------
# Binary comparisons operations
# -------------------------

def p_operation_cmp(p):
    """cmp : operation '<' operation
           | operation '>' operation"""


def p_operation_cmp_eq(p):
    """cmp : operation EQ operation
           | operation NEQ operation"""


def p_operation_cmp_geq(p):
    """cmp : operation GEQ operation
           | operation LEQ operation"""


def p_operation_group(p):
    """operation : '(' operation ')'"""


scanner = scanner.lexer
parser = yacc.yacc()
