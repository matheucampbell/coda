import struct

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

class HeaderChunk:
    '''MIDI Header Chunk'''
    ID = b"MThd"
    def __init__(self, tpq=480):
        self.fmt = 0
        self.ntracks = 1
        self.div = tpq

    def bytes(self):
        '''Returns the binary representation of the header chunk'''
        chunk_length = 6
        fmt = self.fmt
        ntracks = self.ntracks
        div = self.div
        return struct.pack('>4sIHHH', self.ID, chunk_length, fmt, ntracks, div)

class TrackChunk:
    '''MIDI Track Chunk'''
    ID = b"MTrk"
    def __init__(self, tpq=480):
        self.events = b""
        self.tpq = tpq
        self.rest_ticks = 0  # For properly tracking rests

    def add_note(self, note, dur):
        '''Adds a note (in string format) for a given duration (in beats)'''
        ticks_duration = int(dur*self.tpq)  # Convert beats to ticks

        if note == '_':  # On rest, increment current delay and continue
            self.rest_ticks += int(dur*self.tpq)
            return

        note_number = NOTE_MAP[note]
        # Note-on event
        self.events += encode_vlq(self.rest_ticks)  # For proper rest behavior
        self.events += struct.pack(">BBB", 0x90, note_number, 64)  # Note-on (velocity 64)
        self.rest_ticks = 0

        # Note-off event
        self.events += encode_vlq(ticks_duration)  # Delta time
        self.events += struct.pack(">BBB", 0x80, note_number, 0)  # Note-off (velocity 0)
    
    def add_chord(self, chord, dur):
        '''Adds a chord (in string format) for a given duration (in beats)'''
        pass

    def add_meta_event(self, meta_type, data):
        '''Adds a meta event'''
        self.events += struct.pack(">B", 0)  # Delta time: 0
        self.events += struct.pack(">BB", 0xFF, meta_type)  # Meta type
        self.events += struct.pack(">B", len(data)) + data  # Meta event length and data

    def end_track(self):
        '''Adds the End of Track meta-event'''
        self.add_meta_event(0x2F, b"")

    def bytes(self):
        '''Returns the binary representation of the track chunk'''
        chunk_length = len(self.events)
        return struct.pack(">4sI", self.ID, chunk_length) + self.events

class Generator:
    def __init__(self, tempo, note_seq, dur_seq, tpq=480):
        self.header = HeaderChunk(tpq)
        self.track = TrackChunk(tpq)
        self.note_seq = note_seq
        self.dur_seq = dur_seq
        self.tempo = tempo
    
    def generate(self, fname):
        tempo_data = struct.pack(">I", int(60000000 / self.tempo))[1:]
        self.track.add_meta_event(0x51, tempo_data)

        for num, note in enumerate(self.note_seq):
            self.track.add_note(note, self.dur_seq[num])

        self.track.end_track()

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

nseq = ['F4', 'G#4', '_', 'F4']
dseq = [1, 1, 1, 1]
tempo = 120

gen = Generator(tempo, nseq, dseq)
gen.generate('demo')