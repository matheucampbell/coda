from codalexer import Token
from typing import List

symbol_map = {  # Maps production names to descriptions
    '!' : 'GLOBAL FLAG',
    'K': 'KEYSIG MODIFIER',
    'M': 'TIMESIG MODIFIER',
    'D': 'TEMPO MODIFIER',
    'C': 'NOTE BLOCK',
    'T': 'DURATION MODIFIER',
    'R': 'REPETION MODIFIER',
    'G': 'GROUPING MODIFIER',
    'W': 'NOTE/CHORD'
}

class Parser:
    def __init__(self, input: List[Token], parse_table, start_sym):
        self.pos = 0  # Position in list of input tokens
        self.input = input
        input.append(Token('EOF', '$'))
        self.fderived = []
        self.derived = (start_sym,)  # Derived string, list of Tokens and strings (productions)
        self.ptab = parse_table
        
        # AST
        self.nodables = parse_table.get_nodables()
        self.root = ProductionNodeAST("CODA SHEET")
        self.nodestack = [self.root]
        self.closestack = []  # To end a currently open
    
    def parse(self):
        while False in [isinstance(n, Token) for n in self.derived]:
            self.advance()
        print_ast(self.root)

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
            if expanded in self.nodables:
                print("Nodable found:", expanded)
                print("Closing symbol:", expanded[-1])
                node = ProductionNodeAST(symbol_map[cur_sym])
                self.nodestack[-1].add_child(node)
                closesym = expanded[-1]
                self.closestack.append(closesym)
                self.nodestack.append(node)

        else:  # Match token
            # print(f"Attempting to match {str(cur_tok)}")
            if cur_tok.equals(cur_sym):
                self.fderived.append(self.derived[0])
                self.derived = self.derived[1:]
                self.pos += 1
                # print("Matched successfully.")

                # Add as child on current node; close if necessary
                node = TokenNodeAST(cur_tok)
                self.nodestack[-1].add_child(node)
                
                if self.closestack and cur_tok.equals(self.closestack[-1]):
                    # print("Closing symbol found")
                    # print("CHILDREN AT CLOSING:", self.nodestack[-1].children)
                    # print(self.root.children)
                    self.nodestack.pop()
                    self.closestack.pop()
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

    def register_entry(self, coord, rhs, nodable=False):
        '''Add a cell to the table.'''
        self.entries[coord] = rhs  # RHS should be list of tokens or production names
        if nodable:
            self.nodables.add(rhs)

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
    
    def get_nodables(self):
        return self.nodables


class Production:
    """
    Represents a production rule. For special production rules that should be expanded to
    nodes in the AST, nodable=True 
    """
    def __init__(self, symbol, rules):
        self.symbol = symbol
        self.rules = rules


class ProductionNodeAST:
    """AST node for a given production"""
    def __init__(self, value):
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self):
        return f"{self.value}"


class TokenNodeAST:
    """Leaf node of AST"""
    def __init__(self, token):
        self.tok = token
        self.children = []
    
    def __repr__(self):
        return f"{self.tok.text}"


def print_ast(node, level=0, is_last=True, prefix=""):
    if level == 0:
        print(repr(node))
    else:
        connector = "└── " if is_last else "├── "
        print(prefix + connector + repr(node))
    
    prefix += "    " if is_last else "│   "
    
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        is_child_last = (i == child_count - 1)
        print_ast(child, level + 1, is_child_last, prefix)


class ParserException(Exception):
    pass