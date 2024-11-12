from ..Lexer import Token

from typing import List


class Parser:
    def __init__(self, input: List[Token], parse_table):
        self.pos = 0
        self.lookahead = input[self.pos]
        self.ptab = parse_table
        self.derived = []  # List of Token or Production


class ParseTable:  # LL(1) Parsing
    def __init__(self, productions):
        self.entries = {}  # {(nonterminal, Token) : Production, ...}
        self.prods = productions

    def register_entry(self):
        '''Add a cell to the table.'''
        pass

    def get_production(current_nonterm, lookahead: Token):
        '''
        Returns production to take given current nonterminal and lookahead.
        If entry is not found, return None. Caller handles error.
        '''


class Production:
    def __init__(self, symbol, rules):
        self.symbol = symbol
        self.rules = rules


class AbstractSyntaxTree:
    def __init__(self):
        pass