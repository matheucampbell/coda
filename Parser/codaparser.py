from codalexer import Token
from typing import List


class Parser:
    def __init__(self, input: List[Token], parse_table, start_sym):
        self.pos = 0  # Position in list of input tokens
        self.input = input
        input.append(Token('EOF', '$'))
        self.fderived = []
        self.derived = (start_sym,)  # Derived string, list of Tokens and strings (productions)
        self.ptab = parse_table
        
        # AST
        self.root = ProductionNodeAST("Sheet")
        self.nodestack = [self.root]
        self.topnode = self.nodestack[-1]
    
    def parse(self):
        while False in [isinstance(n, Token) for n in self.derived]:
            self.advance()

    def advance(self):
        # self.print_derived()
        cur_tok = self.input[self.pos]  # Token object
        cur_sym = self.derived[0]  # Token or string
        if not isinstance(cur_sym, Token):  # is a production
            if cur_sym == '_':
                self.derived = self.derived[1:]
                return
            
            # print(f"Expanding '{cur_sym}'; Looking at '{cur_tok}'")
            expanded = self.ptab.get_production(cur_sym, cur_tok)
            if not expanded:
                raise ParserException(f"ParseError: No applicable production for current symbol {cur_sym} and next token {cur_tok}.")
            # print(f"Expanded to {expanded}")
            self.derived = expanded + self.derived[1:]  # Should be list of tokens and strings
            # Check if chosen production is nodable


        else:  # Match token
            # print(f"Attempting to match {str(cur_tok)}")
            if cur_tok.equals(cur_sym):
                self.fderived.append(self.derived[0])
                self.derived = self.derived[1:]
                self.pos += 1
                # print("Matched successfully.")
            else:  # Error
                raise ParserException(f"ParseError: Failed to match {cur_tok}. Expected {cur_sym}")

    def print_derived(self):
        s = ""
        for val in self.fderived:
            s += val if not isinstance(val, Token) else val.text
        if s:
            print(f"TD: {s}")

        s = ""
        for val in self.derived:
            s += val if not isinstance(val, Token) else val.text
        print(f"OD: {s}")


class ParseTable:  # LL(1) Parsing
    def __init__(self):
        self.entries = {}  # {(nonterminal, Token) : Production, ...}
        self.nodables = set()

    def register_entry(self, coord, rhs):
        '''Add a cell to the table.'''
        self.entries[coord] = rhs  # RHS should be list of tokens or production names

    def get_production(self, nonterm, lookahead: Token):
        '''
        Returns production to take given current nonterminal and lookahead.
        If entry is not found, return None. Caller handles error.
        '''
        # print(f"Fetching: {nonterm, lookahead}")
        for e in self.entries.keys():
            # print(e, lookahead)
            if e[0] == nonterm and lookahead.equals(e[1]):
                return self.entries[e]
        return None


class Production:
    """
    Represents a production rule. For special production rules that should be expanded to
    nodes in the AST, nodable=True 
    """
    def __init__(self, symbol, rules, nodable=False, closing_symbol=None):
        self.symbol = symbol
        self.rules = rules
        self.nodable = nodable


class ProductionNodeAST:
    """AST node for a given production"""
    def __init__(self, value, closing_token=None):
        self.value = value
        self.children = []
        self.ctoken = closing_token
    
    def add_child(self, child):
        self.children.append(child)


class TokenNodeAST:
    """Leaf node of AST"""
    def __init__(self, token):
        self.value = token


class ParserException(Exception):
    pass