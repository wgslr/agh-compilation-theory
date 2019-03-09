#!/usr/bin/python

import sys
import ply.lex as lex

literals = "+-*/=()[]{}:',;<>"

tokens = ('ELEMWISE_PLUS', 'ELEMWISE_MINUS', 'ELEMWISE_MUL', 'ELEMWISE_DIV',
          'ASSIGN_PLUS', 'ASSIGN_MINUS', 'ASSIGN_MUL', 'ASSIGN_DIV', 'LEQ',
          'GEQ', 'NEQ', 'EQ', 'NUMBER', 'FLOAT', 'ID', 
          )

t_ELEMWISE_PLUS = r'\.+'
t_ELEMWISE_MINUS = r'\.+'
t_ELEMWISE_MUL = 'r\.\*'
t_ELEMWISE_DIV = 'r\./'

t_ASSIGN_PLUS = r'\+='
t_ASSIGN_MINUS = r'-='
t_ASSIGN_MUL = r'\*='
t_ASSIGN_DIV = r'/='

t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='

#t_STRING = r'.+'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
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
