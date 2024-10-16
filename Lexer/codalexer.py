class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"<{self.name}, VALUE={self.value}>"


class Lexer:
    def __init__(self, input_path):
        self.input = self.read_input(input_path)
        self.position = 0
        self.tokens = []

    def tokenize(self):
        '''Tokenizes input string'''
        pass

    def get_tokens(self):
        '''Returns list of tokens after lexing.'''
        pass

    def advance(self):
        '''Advances to next character in text stream'''
        pass


class LexerException(Exception):
    pass
