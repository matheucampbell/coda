from ..Lexer import Token

from typing import List


class Parser:
    def __init__(self, input: List[Token], parse_table):
        self.pos = 0
        self.lookahead = input[self.pos]
        self.derived = []  # Derived string
        self.ptab = parse_table

    def advance(self):
        cur_tok = self.lookahead
        cur_sym = self.derived[self.pos]
        if cur_sym.isinstance(Production):  # Expand production
            self.derived.insert(0, self.ptab(cur_sym, cur_tok))
        else:  # Match token
            if cur_tok.equals(cur_sym):  # Need to write equals() method for Token class to deal with keywords
                self.pos += 1
            else:  # Error
                pass


class ParseTable:  # LL(1) Parsing
    def __init__(self, productions):
        self.entries = {}  # {(nonterminal, Token) : Production, ...}

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