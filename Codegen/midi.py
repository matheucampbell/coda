import struct

# Format Specification: https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BM0_

def encode_vlq(value):
    '''Encodes an integer into a Variable-Length Quantity (VLQ)'''
    buffer = value & 0x7F
    while (value := value >> 7):
        buffer <<= 8
        buffer |= (value & 0x7F) | 0x80
    vlq = bytearray()
    while True:
        vlq.append(buffer & 0xFF)
        if buffer & 0x80:
            buffer >>= 8
        else:
            break
    return bytes(vlq)

def convert_tempo(tempo):
    '''Converts tempo in bpm to ticks per quarter-note'''
    tpq = 480  # Typical, but varies
    microseconds_per_beat = 60000000 / tempo  # microseconds per beat (1 minute / BPM)
    ticks_per_quarter_note = microseconds_per_beat / (60000000 / tpq)  # microseconds_per_beat / microseconds_per_tick

    return int(ticks_per_quarter_note)


class HeaderChunk:
    '''MIDI header chunk'''
    ID = b"MThd"
    def __init__(self, tempo):
        self.fmt = 0
        self.ntracks = 1
        self.div = convert_tempo(tempo)

    def bytes(self):
        '''Returns the 14-bit binary equivalent of header'''
        chunk_length = 6
        fmt = self.fmt
        ntracks = self.ntracks
        div = self.div

        return struct.pack('>4sIHHH', self.ID, chunk_length, fmt, ntracks, div)


class TrackChunk:
    '''MIDI Track Chunk'''
    ID = b"MTrk"
    def __init__(self, tpq=480):
        self.notes = b""
        self.tpq = tpq

    def add_note(self, note, dur):
        '''Adds a note (in string format) for a given duration (in beats)'''
        note_number = NOTE_MAP[note]
        ticks_duration = int(dur * self.tpq)  # Convert beats to ticks
        
        # Encode delta time for the note-on event
        self.notes += struct.pack(">B", 0)
        self.notes += struct.pack(">BBB", 0x90, note_number, 64)  # Note-on (velocity 64)
        
        # Encode delta time for the note-off event
        self.notes += encode_vlq(ticks_duration)  # Delta time (variable length)
        self.notes += struct.pack(">BB", 0x80, note_number)  # Note-off (velocity 0)

    def add_chord(self, notes, dur):
        pass
    
    def bytes(self):
        header = self.ID + struct.pack(">I", len(self.notes))
        return header + self.notes


class Generator:
    def __init__(self, tempo, note_seq, dur_seq):
        self.header = HeaderChunk(tempo)
        self.track = TrackChunk()
        self.note_seq = note_seq
        self.dur_seq = dur_seq
    
    def generate(self, fname):
        for num, note in enumerate(self.note_seq):
            self.track.add_note(note, self.dur_seq[num])

        with open(f'{fname}.mid', "wb") as midi:
            midi.write(self.header.bytes())
            midi.write(self.track.bytes())


# Note Map - Maps text notes from C1 to C5 (sharps specified as ex. C#1 and flats as ex. Cb1)
NOTE_MAP = {
    "C1": 12, "C#1": 13, "Db1": 13, "D1": 14, "D#1": 15, "Eb1": 15,
    "E1": 16, "F1": 17, "F#1": 18, "Gb1": 18, "G1": 19, "G#1": 20, "Ab1": 20,
    "A1": 21, "A#1": 22, "Bb1": 22, "B1": 23, "C2": 24, "C#2": 25, "Db2": 25,
    "D2": 26, "D#2": 27, "Eb2": 27, "E2": 28, "F2": 29, "F#2": 30, "Gb2": 30,
    "G2": 31, "G#2": 32, "Ab2": 32, "A2": 33, "A#2": 34, "Bb2": 34, "B2": 35,
    "C3": 36, "C#3": 37, "Db3": 37, "D3": 38, "D#3": 39, "Eb3": 39, "E3": 40,
    "F3": 41, "F#3": 42, "Gb3": 42, "G3": 43, "G#3": 44, "Ab3": 44, "A3": 45,
    "A#3": 46, "Bb3": 46, "B3": 47, "C4": 48, "C#4": 49, "Db4": 49, "D4": 50,
    "D#4": 51, "Eb4": 51, "E4": 52, "F4": 53, "F#4": 54, "Gb4": 54, "G4": 55,
    "G#4": 56, "Ab4": 56, "A4": 57, "A#4": 58, "Bb4": 58, "B4": 59, "C5": 60
}

# Chord Map - Maps chords to lists of notes from C1 to C5 (supports major and minor | Ex. C-sharp major = C#+ and C-flat minor = ex. Cb-)
CHORD_MAP = {

}

nseq = ['F4', 'A#4', 'F4']
dseq = [2, 2, 2]
tempo = 120

gen = Generator(tempo, nseq, dseq)
gen.generate('demo')