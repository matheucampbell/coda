import struct

# Format Specification: https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BM0_


class HeaderChunk:
    '''MIDI header chunk'''
    ID = b"MThd"
    def __init__(self, tempo):
        self.fmt = 0
        self.ntracks = 1
        self.div = self._convert_tempo(tempo)
    
    def _convert_tempo(self, tempo):
        '''Converts tempo in bpm to ticks per quarter-note'''
        tpq = 480  # Typical, but varies
        microseconds_per_beat = 60000000 / tempo  # microseconds per beat (1 minute / BPM)
        ticks_per_quarter_note = microseconds_per_beat / (60000000 / tpq)  # microseconds_per_beat / microseconds_per_tick

        return int(ticks_per_quarter_note)

    def bytes(self):
        '''Returns the 14-bit binary equivalent of header'''
        chunk_length = 6
        fmt = self.fmt
        ntracks = self.ntracks
        div = self.div

        return struct.pack('>4sIHHH', self.ID, chunk_length, fmt, ntracks, div)


class TrackChunk:
    '''MIDI Track Chunk'''
    def __init__(self):
        self.notes = b""

    def add_note(self, note, dur):
        pass
    
    def bytes(self):
        header = self.ID + struct.pack(">I", len(self.notes))
        return header + self.notes


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

header = HeaderChunk(160)
header.bytes()