class Token:
    '''Instance of a particular token type
    
    Parameters
    ----------
    token_class: str
        Name of type of token this object is
    text: str
        Actual token's text
    valid: bool
        Whether or not text is a valid instance of token_class
    fails: list
        Which DFA stages this token failed on, if any
    '''
    def __init__(self, token_class, text, fails=[]):
        self.token_class = token_class
        self.text = text
        self.valid = not fails
        self.fails = fails
    
    def __repr__(self):
        return f"<{self.token_class}, VALUE='{self.text}', VALID={self.valid}>"


class Regex:
    '''Custom regular expression class'''
    def __init__(self, token_class, text_re, stage_dict, 
                 optionals=[], repeats=[], inverts=[], single=False):
        self.textexp = text_re
        self.tclass = token_class
        self.stages = stage_dict
        self.opts = optionals
        self.reps = repeats
        self.invs = inverts
        self.final = max(set(stage_dict.keys()) - set(optionals))  # Final stage
        self.max_stage = max(stage_dict.keys())
        self.single = single

    def search(self, input):
        '''Search for a match in given input'''
        return self.match(input)
    
    def match(self, input):
        '''Returns Token object for a given input, None if invalid'''
        failed = []  # Failed stages
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
            else:  # Required stage not matched
                failed.append(stage)
                stage += 1
        
        # Check that final stage was reached
        if stage - 1 >= self.final:
            # print(self.tclass, self.failed, input[:i].strip('\n'))
            return Token(self.tclass, input[:i].strip('\n'), fails=failed)
        # print(f"Minimum final stage not reached. Current stage: {stage}")
        return Token(self.tclass, input[:i].strip('\n'), fails=failed)
    
    def __repr__(self):
        return f"<REGEX, TEXTEXP={self.textexp}, STAGEDICT={self.stages}>"


class Lexer:
    def __init__(self):
        self.position = 0
        self.tokens = []  # Matched tokens
        self.token_bank = []  # Valid regexes
        self.singles = []  # Single-character tokens
        self.input = ""

    def register_token(self, regex):
        '''Adds a recognized token type.'''
        self.token_bank.append(regex)
        if regex.single:
            self.singles.append(regex.tclass)

    def tokenize(self, input_path):
        '''Tokenizes the entire input string.'''
        with open(input_path, 'r') as infile:
            self.input = infile.read()
        
        self.skip_whitespace()
        while self.position < len(self.input):
            self.exec_dfa()
            self.skip_whitespace()

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
        
        valids = [m for m in matches if m.valid]
        if not valids:
            if self.position+10 < len(self.input) - 1:
                inp_slice = "'" + self.input[self.position:self.position+10] + '...' + "'"
            else:
                inp_slice = self.input[self.position:]
            line, col = self.pos_to_coord(self.position)

            # Correction suggestion: If exactly one character failed, suggest a correction.
            # If exactly one character failed for multiple possible tokens, choose the longest.
            # Exclude tokens that can be single characters.
            almost = [m for m in matches if len(m.fails) == 1 and m.token_class not in self.singles]
            if almost:
                failures = [len(m.text) for m in almost]
                zipped = zip(almost, failures)
                csugg = sorted(zipped, key=lambda x: x[1])[-1][0]

                # print(f"{len(almost)} single-stage failures found.")
                raise LexerException(f"Malformed token found. For {csugg.token_class} token, correct stage {csugg.fails[0]} of input on line {line}, column {col}: {inp_slice}")
            else:
                raise LexerException(f"Unrecognized symbol or token on line {line}, column {col}: {inp_slice}")
        
        # Maximal munch
        matchlens = [len(m.text) for m in valids]
        zipped = zip(valids, matchlens)
        match = sorted(zipped, key=lambda x: x[1])[-1][0]

        self.tokens.append(match)
        self.position += len(match.text)
        return

    def pos_to_coord(self, pos):
        '''Convert position in input to line number, column number'''
        lines = self.input[:pos].splitlines()
        line_num = len(lines)
        col_num = len(lines[-1]) + 1 if lines else 1

        return line_num, col_num

    def __exit__(self):
        '''Ensures the input file is closed.'''
        if not self.infile.closed:
            self.infile.close()


class LexerException(Exception):
    pass
