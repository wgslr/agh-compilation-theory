#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens
literals = scanner.literals


precedence = (
    ('left', 'IF'),
    ('left', 'ELSE'),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('left', '<', '>', 'EQ', 'NEQ', 'GEQ', 'LEQ'),
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

def p_many_expressions(_p):
    """many_expressions : expression
                       | expression many_expressions"""


def p_expr(_p):
    """expression : block
                  | base_expr
                  | if_statement
                  | loop"""


def p_base_expr(_p):
    """base_expr : assignment ';'
                 | return ';'
                 | print ';'"""


def p_cond(_p):
    """cond : cmp
            | operation"""


def p_operation(_p):
    """operation : num
                 | unary_op
                 | fun"""


def p_block(_p):
    """block : '{' many_expressions '}'"""


def p_print(_p):
    """print : PRINT print_body"""


def p_print_body(_p):
    """print_body : STRING
                  | cond
                  | print_body ',' cond"""


def p_return(_p):
    """return : RETURN cond
              | RETURN """


# -------------------------
# Matrices
# -------------------------

def p_vector(_p):
    """vector : '[' vector_body ']'"""


def p_vector_body(_p):
    """vector_body : num
                   | vector_body ',' num
                   | empty"""


def p_matrix(_p):
    """matrix : '[' matrix_body ']'"""


def p_matrix_body(_p):
    """matrix_body : vector
                   | matrix_body ',' vector
                   | empty"""


# -------------------------
# Arrays
# -------------------------

def p_array_range(_p):
    """array_range : ID '[' int_num_var ',' int_num_var ']'"""


# -------------------------
# Funs
# -------------------------

def p_fun(_p):
    """fun : fun_name '(' num ')'"""


def p_fun_name(_p):
    """fun_name : ZEROS
                | ONES
                | EYE"""


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
                 | '{' many_loop_expr '}'"""


def p_loop_expr(_p):
    """loop_expr : base_expr
                 | loop
                 | if_loop_statement
                 | BREAK ';'
                 | CONTINUE ';'"""


def p_many_loop_expr(_p):
    """many_loop_expr : many_loop_expr loop_expr
                     | loop_expr"""


# -------------------------
# If statements
# -------------------------

def p_if_statement(_p):
    """if_statement : IF '(' cond ')' expression %prec IF
                    | IF '(' cond ')' expression ELSE expression"""


def p_if_loop_statement(_p):
    """if_loop_statement : IF '(' cond ')' loop_body %prec IF
       if_loop_statement : IF '(' cond ')' loop_body ELSE loop_body"""


def p_empty(_p):
    """empty : """


# -------------------------
# Assignments
# -------------------------

def p_assignee(_p):
    """assignee : ID
                | array_range"""


def p_assignment(_p):
    """assignment : assignee '=' cond
                  | assignee '=' matrix
                  | assignee '=' STRING"""


def p_addassignment(_p):
    """assignment : assignee ADDASSIGN cond"""


def p_subassignment(_p):
    """assignment : assignee SUBASSIGN cond"""


def p_mulassignment(_p):
    """assignment : assignee MULASSIGN cond"""


def p_divassignment(_p):
    """assignment : ID DIVASSIGN cond"""


# -------------------------
# Numeric and variables
# -------------------------

def p_var(_p):
    """var : ID"""


def p_num(_p):
    """num : INTNUM 
           | FLOATNUM
           | var"""


def p_int_num_var(_p):
    """int_num_var : INTNUM
                   | var"""


# -------------------------
# Unary operations
# -------------------------

def p_unary_op(_p):
    """unary_op : neg_num
                | transpose"""


def p_neg(_p):
    """neg_num : '-' num %prec UMINUS"""


def p_transpose(_p):
    """transpose : operation '\\'' """


# -------------------------
# Binary operations
# -------------------------

def p_operation_sum(_p):
    """operation : operation '+' operation
                 | operation '-' operation"""


def p_operation_dot_sum(_p):
    """operation : operation DOTADD operation
                 | operation DOTSUB operation"""


def p_operation_mul(_p):
    """operation : operation '*' operation
                 | operation '/' operation"""


def p_operation_dot_mul(_p):
    """operation : operation DOTMUL operation
                 | operation DOTDIV operation"""


# -------------------------
# Binary comparisons operations
# -------------------------

def p_operation_cmp(_p):
    """cmp : operation '<' operation
           | operation '>' operation"""


def p_operation_cmp_eq(_p):
    """cmp : operation EQ operation
           | operation NEQ operation"""


def p_operation_cmp_geq(_p):
    """cmp : operation GEQ operation
           | operation LEQ operation"""


def p_operation_group(_p):
    """operation : '(' operation ')'"""


parser = yacc.yacc()
