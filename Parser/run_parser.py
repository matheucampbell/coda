from lex import lexer
from parse import Parser, parse_table

import argparse
import sys

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', '--input-file', required=True, help='Input file for lexing')

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
