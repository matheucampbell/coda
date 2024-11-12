from codaparser import *
from lex import lexer

import argparse
import sys

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input-file', required=True, help='Input file for lexing')

args = argparser.parse_args()

# Run lexer
try:
    lexer.tokenize(args.input_file)
except FileNotFoundError:
    print(f"Invalid file path supplied: '{args.input_file}'")
    sys.exit()

token_list = lexer.get_tokens()

# Run parser
# Define dummy tokens for comparison
eof = Token('EOF', '$')
note = Token('NOTE', '-')
chord = Token('CHORD', '-')
keysig = Token('KEY', '-')
declarator = Token('DECLARATOR', '!')
sep = Token('SEPARATOR', ',')
lbrace = Token('LBRACE', '{')
rbrace = Token('RBRACE', '}')
lbracket = Token('LBRACKET', '[')
rbracket = Token('RBRACKET', ']')
number = Token('NUMBER', '-')   
key = Token('KEYWORD', 'key')
sig = Token('KEYWORD', 'sig')
tmp = Token('KEYWORD', 'tmp')
typ = Token('KEYWORD', 'typ')
rep = Token('KEYWORD', 'rep')
grp = Token('KEYWORD', 'grp')
conn = Token('CONNECTOR', '>')
cconn = Token('CONNECTOR', '>>')

# Create productions
S = Production('S', {0: ['I', 'B']})
I = Production('I', {0: [declarator, 'K', declarator, 'M', declarator, 'D']})
K = Production('K', {0: [key, lbracket, keysig, rbracket]})
M = Production('M', {0: [sig, lbracket, number, sep, number, rbracket]})
D = Production('D', {0: [tmp, lbracket, number, rbracket]})
B = Production('B', {0: ['C', 'Bp']})
Bp = Production('Bp', {0: ['C', 'Bp'], 1: ['_']})
C = Production('C', {0: ['T', 'R', 'G', lbrace, 'B', rbrace], 1: ['N']})
T = Production('T', {0: [typ, lbracket, number, rbracket], 1: ['_']})
R = Production('R', {0: [rep, lbracket, number, rbracket], 1: ['_']})
G = Production('G', {0: [grp, lbracket, number, rbracket], 1: ['_']})
N = Production('N', {0: ['W', 'Np']})
Np = Production('Np', {0: [conn, 'N'], 1: [cconn, 'N'], 2: ['_']})
W = Production('W', {0: [chord], 1: [note]})

parse_table = ParseTable()
# Populate table
parse_table.register_entry(('S', declarator), S.rules[0])
parse_table.register_entry(('I', declarator), I.rules[0])
parse_table.register_entry(('K', key), K.rules[0])
parse_table.register_entry(('M', sig), M.rules[0])
parse_table.register_entry(('D', tmp), D.rules[0])
parse_table.register_entry(('B', note), B.rules[0])
parse_table.register_entry(('B', chord), B.rules[0])
parse_table.register_entry(('B', typ), B.rules[0])
parse_table.register_entry(('B', rep), B.rules[0])
parse_table.register_entry(('B', grp), B.rules[0])
parse_table.register_entry(('B', lbrace), B.rules[0])
parse_table.register_entry(('Bp', note), B.rules[0])
parse_table.register_entry(('Bp', chord), B.rules[0])
parse_table.register_entry(('Bp', typ), B.rules[0])
parse_table.register_entry(('Bp', rep), B.rules[0])
parse_table.register_entry(('Bp', grp), B.rules[0])
parse_table.register_entry(('Bp', lbrace), B.rules[0])
parse_table.register_entry(('Bp', rbrace), B.rules[0])
parse_table.register_entry(('Bp', lbrace), ['_'])
parse_table.register_entry(('C', note), C.rules[1])
parse_table.register_entry(('C', chord), C.rules[1])
parse_table.register_entry(('C', typ), C.rules[0])
parse_table.register_entry(('C', rep), C.rules[0])
parse_table.register_entry(('C', grp), C.rules[0])
parse_table.register_entry(('C', lbrace), C.rules[0])
parse_table.register_entry(('C', eof), ['_'])
parse_table.register_entry(('T', typ), T.rules[0])
parse_table.register_entry(('T', rep), ['_'])
parse_table.register_entry(('T', grp), ['_'])
parse_table.register_entry(('T', lbrace), ['_'])
parse_table.register_entry(('R', rep), R.rules[0])
parse_table.register_entry(('R', grp), ['_'])
parse_table.register_entry(('R', lbrace), ['_'])
parse_table.register_entry(('G', grp), G.rules[0])
parse_table.register_entry(('G', lbrace), ['_'])
parse_table.register_entry(('N', note), N.rules[0])
parse_table.register_entry(('N', chord), N.rules[0])
parse_table.register_entry(('Np', note), ['_'])
parse_table.register_entry(('Np', chord), ['_'])
parse_table.register_entry(('Np', typ), ['_'])
parse_table.register_entry(('Np', rep), ['_'])
parse_table.register_entry(('Np', grp), ['_'])
parse_table.register_entry(('Np', lbrace), ['_'])
parse_table.register_entry(('Np', rbrace,), ['_'])
parse_table.register_entry(('Np', eof), ['_'])
parse_table.register_entry(('Np', conn), Np.rules[0])
parse_table.register_entry(('Np', cconn), Np.rules[1])
parse_table.register_entry(('W', note), W.rules[0])
parse_table.register_entry(('W', chord), W.rules[1])
parse_table.register_entry(('W', eof), ['_'])

parser = Parser(token_list, parse_table, 'S')
parser.parse()
