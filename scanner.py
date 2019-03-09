#!/usr/bin/python

import sys
import ply.lex as lex
literals = "+-*/=()[]{}:',;<>"

tokens = ('DOTSUM', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          'SUMASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'LEQ',
          'GEQ', 'NEQ', 'EQ', 'INTNUM', 'FLOATNUM', 'ID', 
          )

t_DOTSUM = r'\.+'
t_DOTSUB = r'\.+'
t_DOTMUL = 'r\.\*'
t_DOTDIV = 'r\./'

t_SUMASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='

#t_STRING = r'.+'

t_ignore = ' \t'

def t_FLOATNUM(t):
    r'[+-]?\d*\.\d+([eE][+-]?\d+)?'
    print(t.value)
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'[+-]?\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

def t_comment(t):
    r'\#.*'
    pass


def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

lexer = lex.lex()
fh = None
