from midi import MidiGenerator

class CodaGenerator:
    def __init__(self, ast_root, outname='output'):
        self.root = ast_root
        self.outname = outname
        self.typstack = [1]
        self.repstack = [1]
        self.grpstack = [1]
        self.keysig = None
        self.timesig = None
        self.tempo = None
    
    def generate(self):
        tokens, durations = self.get_sequences()
        gen = MidiGenerator(self.tempo, tokens, durations)
        gen.generate(self.outname)
    
    def get_sequences(self):
        '''Parses AST to generate input for MidiGenerator'''
        # 1. Pass 1: Get global identifiers
        next_node = self.get_globals()

        return [], []
        import sys
        sys.exit()

        # 2. Track current modifiers on relevant stacks and recursively process note blocks
        # Stacks initialized to typ=1, rep=1, grp=1
    
    def get_globals(self):
        '''Extract global identifiers. Treat the rest of the program as one note block.'''
        # Can hardcode locations of global identifiers
        self.keysig = self.root.children[1].children[2]
        self.timesig = [self.root.children[3], self.root.children[5]]
        self.tempo = self.root.children[5].children[2]

    def parse_block(self, node):
        '''Parse a note block'''
        # typ not None -> All notes have specified duration
        # rep not None -> Entire block repeated as specified
        # grp not None -> Group first n notes in block
        note_seq = []
        dur_seq = []

        for child in node.children:
            while child.value != 'NOTE BLOCK':
                if child.value == 'typ':
                    pass
                elif child.value == 'rep':
                    pass
                elif child.value == 'grp':
                    pass
                elif child.value == 'NOTE' or child.value == 'CHORD':
                    pass
            else:
                ns, ds = self.parse_block(node)
                note_seq += ns
                dur_seq += ds
