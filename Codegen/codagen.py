from codaparser import TokenNodeAST, ProductionNodeAST
from midi import MidiGenerator

class CodaGenerator:
    def __init__(self, ast_root, outname='output'):
        self.root = ast_root
        self.outname = outname
        self.typstack = []
        self.repstack = []
        self.grpstack = []
        self.keysig = None
        self.timesig = None
        self.tempo = None
    
    def generate(self):
        tokens, durations = self.get_sequences()
        gen = MidiGenerator(self.tempo, tokens, durations)
        gen.generate(self.outname)
    
    def get_sequences(self):
        '''Parses AST to generate input for MidiGenerator'''
        # 1. Step 1: Get global modifiers
        next_node = self.get_globals()
        return self.parse_block(next_node, 1, 1, 1)

    def get_globals(self):
        '''Extract global identifiers. Treat the rest of the program as one note block.'''
        # Can hardcode locations of global identifiers
        self.keysig = self.root.children[1].children[2]
        self.timesig = [self.root.children[3].children[2], self.root.children[3].children[4]]
        self.tempo = self.root.children[5].children[2]

        # TODO: Proceed through the rest of the tree and find all global identifiers 

        return self.root.children[7]

    def parse_block(self, node, typ, rep, grp):
        '''Parse a note block'''
        # typ[n] -> All notes have specified duration
        # rep[n] -> Entire block repeated as specified
        # grp[n] -> Group first n notes in block

        # Update stacks with current level's modifiers
        self.typstack.append(typ)
        self.repstack.append(rep)
        self.grpstack.append(grp)

        # Initialize next level's mods (overwritten if found)
        next_typ = self.typstack[-1]  # typ modifier inherited by enclosed blocks
        next_rep = 1  # rep modifier NOT inherited by enclosed blocks
        next_grp = 1  # grp modifier NOT inherited by enclosed blocks

        note_seq, dur_seq = [], []

        print("NODE: ", node, node.children)
        for child in node.children:
            if isinstance(child, TokenNodeAST):
                if child.tok.token_class != 'CHORD' and child.tok.token_class != 'NOTE':
                    continue
            
            if child.value != 'NOTE BLOCK':
                if child.value == 'DURATION MODIFIER':
                    next_typ = child.children[2]
                elif child.value == 'REPETITION MODIFIER':
                    next_rep = child.children[2]
                elif child.value == 'GROUPING MODIFIER':
                    next_grp = child.children[2]
                elif child.value == 'NOTE/CHORD/REST':
                    # Use current duration modifier to add values to notes
                    note_seq.append(child.children[0])
                    dur_seq.append(self.typstack[-1])
            else:
                ns, ds = self.parse_block(node, next_typ, next_rep, next_grp)
                note_seq += ns
                dur_seq += ds
        
        note_seq = note_seq * self.repstack[-1]
        dur_seq = dur_seq * self.repstack[-1]

        self.typstack.pop()
        self.repstack.pop()
        self.grpstack.pop()

        return note_seq, dur_seq
