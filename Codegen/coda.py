from lex import lexer
from codaparser import Parser
from parse import parse_table
from codagen import CodaGenerator

import argparse
import sys

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input-file', required=True, help='Input file for MIDI conversion.')
argparser.add_argument('-o', '--output-file', default='output', help='Output file name')

args = argparser.parse_args()

# Lexical Analysis
try:
    lexer.tokenize(args.input_file)
except FileNotFoundError:
    print(f"Invalid file path supplied: '{args.input_file}'")
    sys.exit()

token_list = lexer.get_tokens()

# Synctactic Analysis
parser = Parser(token_list, parse_table, 'S')
parser.parse()

# Code Generation
ast_root = parser.root
gen = CodaGenerator(ast_root, args.output_file)
gen.generate()