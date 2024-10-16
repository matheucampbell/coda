class Token:
    '''Instance of a particular token type'''
    def __init__(self, token_class, text):
        self.token_class = token_class
        self.text = text
    
    def __repr__(self):
        return f"<{self.token_class}, VALUE='{self.text}'>"


class Regex:
    '''Simplified regular expression class'''
    def __init__(self, token_class, text_re, stage_dict, optionals=[]):
        self.textexp = text_re
        self.tclass = token_class
        self.stages = stage_dict
        self.opts = optionals
        self.min_stage = max(set(stage_dict.keys()) - set(optionals))
    
    def search(self, input):
        '''Search for a match in given input'''
        return self.match(input)
    
    def match(self, input):
        '''Returns Token object for a given input, None if invalid'''
        i = 0
        stage = 0
        while i < len(input) and stage <= max(self.stages.keys()):
            if input[i] not in self.opts and input[i] in self.stages[stage]:
                i += 1
                stage += 1
            elif stage in self.opts:
                # print(f"Stage {stage} optional and skipped.")
                stage += 1
            else:  # Stage not matched and not optional
                # print(f"Stage {stage} for {self.tclass} not matched. Current char: {input[i]}")
                # print(input[i], self.opts, self.stages[i])
                return None
        
        # Check that minimum final stage was reached
        if stage - 1 >= self.min_stage:
            return Token(self.tclass, input[:i])
        # print(f"Minimum final stage not reached. Current stage: {stage}")
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
            self.input = self.input.replace(" ", "")
            self.input = "".join(self.input.splitlines())
            # print(self.input)

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
        matches = []
        for regex in self.token_bank:
            matches.append(regex.search(self.input[self.position:]))
        
        # Maximal munch
        matches = [m for m in matches if m]
        if not matches:
            raise LexerException(f"No valid token at position {self.position}: '{self.input[self.position:self.position+10]}...'")
        
        matchlens = [len(m.text) for m in matches]
        zipped = zip(matches, matchlens)
        match = sorted(zipped, key=lambda x: x[1])[-1][0]

        self.tokens.append(match)
        self.position += len(match.text)
        print(match)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Ensures the input file is closed.'''
        if hasattr(self, 'infile') and not self.infile.closed:
            self.infile.close()


class LexerException(Exception):
    pass
