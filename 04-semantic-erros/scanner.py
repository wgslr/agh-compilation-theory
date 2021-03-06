#!/usr/bin/env python2

import sys
import ply.lex as lex
literals = "+-*/=()[]{}:',;<>"


keywords = ('IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE',
            'RETURN', 'EYE', 'ZEROS', 'ONES', 'PRINT')

tokens = ('DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'LEQ',
          'GEQ', 'NEQ', 'EQ', 'INTNUM', 'FLOATNUM', 'STRING', 'ID'
          ) + keywords

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'


def t_FLOATNUM(t):
    # fraction part can be omitted if exponent is present
    r'\d* ((\d\.|\.\d) \d* ([eE][+-]?\d+)? | \d([eE][+-]?\d+))'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


def t_comment(t):
    r'[#].*'
    pass


def t_STRING(t):
    r""""([^"\\\n]|\\.)*" """

    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    if t.value.upper() in keywords:
        t.type = t.value.upper()

    return t


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
fh = None
