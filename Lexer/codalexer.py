class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"<{self.name}, VALUE={self.value}>"


class SimpleRegex:
    '''Simplified regular expression class'''
    def __init__(self, stage_list):
        pass


class Lexer:
    def __init__(self, input_path):
        self.input = self.read_input(input_path)
        self.position = 0
        self.tokens = []

    def register_token(self, name, regex):
        '''Adds a recognized token type'''
        pass

    def tokenize(self):
        '''Tokenizes input string'''
        pass

    def get_tokens(self):
        '''Returns list of tokens after lexing.'''
        pass

    def advance(self):
        '''Advances to next character in text stream'''
        pass

    def exec_dfa(self):
        '''
        Runs DFA starting at current token and appends new token to list.
        Raises exception on lexical error.
        '''
        char = self.input[self.pos]

        # Single-character tokens
        if char in self.singles:
            pass

        # Multi-character processing


class LexerException(Exception):
    pass
