import argparse
import sys

from lex import lexer

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', required=True, help='Input file for lexing')

args = parser.parse_args()

try:
    lexer.tokenize(args.input_file)
except FileNotFoundError:
    print(f"Invalid file path supplied: '{args.input_file}'")
    sys.exit()

for x in lexer.get_tokens():
    print(x)