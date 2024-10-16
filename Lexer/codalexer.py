class Token:
    '''Instance of a particular token type'''
    def __init__(self, token_class, text):
        self.token_class = token_class
        self.text = text
    
    def __repr__(self):
        return f"<{self.token_class}, VALUE='{self.text}'>"


class Regex:
    '''Custom regular expression class'''
    #TODO: Write error cases and sample programs
    def __init__(self, token_class, text_re, stage_dict, 
                 optionals=[], repeats=[], inverts=[]):
        self.textexp = text_re
        self.tclass = token_class
        self.stages = stage_dict
        self.opts = optionals
        self.reps = repeats
        self.invs = inverts
        self.final = max(set(stage_dict.keys()) - set(optionals))  # Final stage
        self.max_stage = max(stage_dict.keys())

    def search(self, input):
        '''Search for a match in given input'''
        return self.match(input)
    
    def match(self, input):
        '''Returns Token object for a given input, None if invalid'''
        i = 0
        stage = 0
        while i < len(input) and stage <= self.max_stage:
            c = input[i]
            valid_chars = self.stages[stage]

            if stage not in self.invs:
                valid = c in valid_chars
            else:
                valid = c not in valid_chars
            
            if stage not in self.opts and stage not in self.reps and valid:
                i += 1
                stage += 1
            elif stage in self.opts:
                if valid: i += 1
                stage += 1
            elif stage in self.reps:
                if valid: i += 1
                else: stage += 1
            else:  # Stage not matched and not optional
                return None
        
        # Check that final stage was reached
        if stage - 1 >= self.final:
            return Token(self.tclass, input[:i].strip('\n'))
        print(f"Minimum final stage not reached. Current stage: {stage}")
        return None
    
    def __repr__(self):
        return f"<REGEX, TEXTEXP={self.textexp}, STAGEDICT={self.stages}>"


class Lexer:
    def __init__(self):
        self.position = 0
        self.tokens = []  # Matched tokens
        self.token_bank = []  # Valid regexes
        self.input = ""

    def register_token(self, regex):
        '''Adds a recognized token type.'''
        self.token_bank.append(regex)

    def tokenize(self, input_path):
        '''Tokenizes the entire input string.'''
        with open(input_path, 'r') as infile:
            self.input = infile.read()
            # self.input = self.input.replace(" ", "")
            # self.input = "".join(self.input.splitlines())
            # print(self.input)

        while self.position < len(self.input):
            self.skip_whitespace()
            self.exec_dfa()

    def get_tokens(self):
        '''Returns list of tokens after lexing.'''
        return self.tokens

    def skip_whitespace(self):
        '''Advances to the next non-newline character in input stream.'''
        while self.position < len(self.input) and \
              (self.input[self.position] == '\n' or self.input[self.position] == ' '):
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
        
        matches = [m for m in matches if m]
        if not matches:
            raise LexerException(f"No valid token at position {self.position}: '{self.input[self.position:min(self.position+10, len(self.input)-1)]}...'")
        
        # Maximal munch
        matchlens = [len(m.text) for m in matches]
        zipped = zip(matches, matchlens)
        match = sorted(zipped, key=lambda x: x[1])[-1][0]

        self.tokens.append(match)
        self.position += len(match.text)
        print(match)
        return

    def __exit__(self):
        '''Ensures the input file is closed.'''
        if not self.infile.closed:
            self.infile.close()


class LexerException(Exception):
    pass
