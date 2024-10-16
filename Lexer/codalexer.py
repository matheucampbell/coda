class Token:
    '''Instance of a particular token type'''
    def __init__(self, token_class, text):
        self.token_class = token_class
        self.text = text
    
    def __repr__(self):
        return f"<{self.token_class}, VALUE={self.text}>"


class Regex:
    '''Simplified regular expression class'''
    def __init__(self, token_class, stage_dict, text_re, optionals=[]):
        self.length = 0
        self.textexp = text_re
        self.tclass = token_class
        self.stages = stage_dict
        self.opts = optionals
    
    def search(self, input):
        '''Search for a match in given input'''
        print("Searching for", self.tclass)
        return self.match(input)
    
    def match(self, input):
        '''Returns Token object for a given input, None if invalid'''
        i = 0
        stage = 0
        while i < len(input) and stage <= max(self.stages.keys()):
            if input[i] not in self.opts and input[i] in self.stages[i]:
                i += 1
                stage += 1
            elif stage in self.opts:
                stage += 1
            else:  # Stage not matched and not optional
                print(f"Stage {stage} for {self.textexp} not matched. Current char: {input[i]}")
                print(input[i], self.opts, self.stages[i])
                return None
        
        # Check that final stage was reached
        if stage - 1 == max(self.stages.keys()):
            return Token(self.tclass, input[:i])
        print(f"Final stage not reached. Current stage: {stage}")
        return None

    
    def __repr__(self):
        return f"<REGEX, TEXTEXP={self.textexp}, STAGEDICT={self.stages}>"


class Lexer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.position = 0
        self.tokens = []  # Matched tokens
        self.token_bank = []  # Valid regexes
        self.input = ""

    def register_token(self, regex):
        '''Adds a recognized token type.'''
        self.token_bank.append(regex)

    def tokenize(self):
        '''Tokenizes the entire input string.'''
        with open(self.input_path, 'r') as infile:
            self.input = infile.read()

        while self.position < len(self.input):
            self.exec_dfa()

    def get_tokens(self):
        '''Returns list of tokens after lexing.'''
        return self.tokens

    def advance(self):
        '''Advances to the next character in the input stream.'''
        self.position += 1

    def exec_dfa(self):
        '''
        Runs the DFA starting at the current position.
        Appends new token to the token list.
        Raises an exception on lexical error.
        '''
        for regex in self.token_bank:
            match = regex.search(self.input[self.position:])
            if match:
                self.tokens.append(match)
                self.position += len(match.text)
                print(match)
                return
        
        raise Exception(f"Lexical error at position {self.position}: '{self.input[self.position]}'")

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Ensures the input file is closed.'''
        if hasattr(self, 'infile') and not self.infile.closed:
            self.infile.close()


class LexerException(Exception):
    pass
