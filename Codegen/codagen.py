from codaparser import TokenNodeAST
from midi import MidiGenerator

class CodaGenerator:
    def __init__(self, ast_root, outname='output'):
        self.root = ast_root
        self.outname = outname
        self.typstack = [1]
        self.keysig = None
        self.timesig = None
        self.tempo = None

        self.globaltyp = 1
        self.globalrep = 1
    
    def generate(self):
        tokens, durations = self.get_sequences()
        gen = MidiGenerator(self.tempo, tokens, durations)
        gen.generate(self.outname)
    
    def get_sequences(self):
        '''Parses AST to generate input for MidiGenerator'''
        # 1. Step 1: Get global modifiers
        self.get_globals()
        return self.parse_block(self.root)

    def get_globals(self):
        '''Extract global identifiers. Treat the rest of the program as one note block.'''
        # Can hardcode locations of global identifiers
        self.keysig = self.root.children[1].children[2]
        self.timesig = [self.root.children[3].children[2], self.root.children[3].children[4]]
        self.tempo = int(self.root.children[5].children[2].tok.text)

    def parse_block(self, node):
        '''Parse a note block'''
        # typ[n] -> All notes have specified duration
        # rep[n] -> Entire block repeated as specified
        # grp[n] -> Group first n notes in block

        # Update stacks with current level's modifiers
        self.typstack.append(self.typstack[-1])  # typ inherited from outer blocks
        rep = 1
        grp = 0
        gcount = 0  # Number of elements counted for the group

        note_seq, dur_seq = [], []

        # print("NODE: ", node, node.children)
        # print(f"CURRENT MODS | typ: {self.typstack[-1]} | rep: {rep} | grp: {grp}")
        for child in node.children:
            # print(f"\tChecking: {child}")
            if isinstance(child, TokenNodeAST):
                if child.tok.token_class != 'CHORD' and child.tok.token_class != 'NOTE':
                    continue
            
            if child.value != 'NOTE BLOCK':
                if child.value == 'DURATION MODIFIER':
                    self.typstack[-1] = int(child.children[2].tok.text)
                elif child.value == 'REPETITION MODIFIER':
                    rep = int(child.children[2].tok.text)
                elif child.value == 'GROUPING MODIFIER':
                    # print("GROUP FOUND")
                    grp = int(child.children[2].tok.text)  # Next note block should be grouped
                elif child.value == 'NOTE/CHORD/REST':
                    # Use current duration modifier to add values to notes
                    note_seq.append(child.children[0].tok)
                    dur_seq.append(self.typstack[-1])
                    if grp:
                        gcount += 1
                        # print("\tINCREMENTING")
            else:
                ns, ds = self.parse_block(child)
                note_seq += ns
                dur_seq += ds

        note_seq = note_seq * rep
        dur_seq = dur_seq * rep
        if grp:
            note_seq.insert(0, gcount)

        self.typstack.pop()

        return note_seq, dur_seq
