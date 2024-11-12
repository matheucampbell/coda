from codaparser import *

# # Define dummy tokens for comparison
# note = Token('NOTE', '_')
# chord = Token('CHORD', '_')
# key = Token('KEY', '_')
# declarator = Token('DECLARATOR', '!')
# sep = Token('SEPARATOR', ',')
# lbrace = Token('LBRACE', '{')
# rbrace = Token('RBRACE', '}')
# lbracket = Token('LBRACKET', '[')
# rbracket = Token('RBRACKET', ']')
# number = Token('NUMBER', '_')   
# keysig = Token('KEYWORD', 'key')
# sig = Token('KEYWORD', 'sig')
# tmp = Token('KEYWORD', 'tmp')
# typ = Token('KEYWORD', 'typ')
# rep = Token('KEYWORD', 'rep')
# grp = Token('KEYWORD', 'grp')
# conn = Token('CONNECTOR', '>')
# cconn = Token('CONNECTOR', '>>')

# # Create productions
# K = Production('K', {0: (key, keysig)})
# M = Production('M', {0: (sig, lbracket, number, sep, number, rbracket)})
# D = Production('D', {0: (tmp, lbracket, number, rbracket)})
# T = Production('T', {0: (typ, lbracket, number, rbracket), 1: ()})
# R = Production('R', {0: (rep, lbracket, number, rbracket), 1: ()})
# G = Production('G', {0: (grp, lbracket, number, rbracket), 1: ()})
# W = Production('W', {0: (chord), 1: (note)})

# I = Production('I', {0: (declarator, K, declarator, M, declarator, D)})
# C = Production('C', {0: (T, R, G, lbrace, B, rbrace), 1: {N}})
