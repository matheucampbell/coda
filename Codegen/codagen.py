from midi import MidiGenerator

class CodaGenerator:
    def __init__(self, ast_root, outname='output'):
        self.root = ast_root
        self.outname = outname
    
    def generate(self):
        tempo, tokens, durations = self.get_sequences()
        gen = MidiGenerator(tempo, tokens, durations)
        gen.generate(self.outname)
    
    def get_sequences(self):
        '''Parses AST to generate input for MidiGenerator'''
        