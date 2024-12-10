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

    def add(self, item, dur):
        if item.token_class == "CHORD":
            self.add_chord(item, dur)
        else:
            self.add_note(item, dur)

    def add_note(self, note, dur):
        '''Adds a note (as an object of class Token) for a given duration (in beats)'''
        note = note.text
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
        '''Adds a chord (as an object class Token) for a given duration (in beats)'''
        chord = chord.text  # Ex: C+5*
        base, oct = chord[:-2], chord[-2]
        notes = CHORD_MAP[base]  # ["C", "E", "G"]

        self.events += encode_vlq(self.rest_ticks)  # Apply rest before playing the chord
        self.events += struct.pack(">BBB", 0x90, NOTE_MAP[notes[0]+oct], 64)
        for note in notes[1:]:
            note_num = NOTE_MAP[note + oct]
            self.events += encode_vlq(0)  # Same time as other notes
            self.events += struct.pack(">BBB", 0x90, note_num, 64)  # Note-on, velocity 64

        self.rest_ticks = 0

        self.events += encode_vlq(int(dur * self.tpq))  # Delta time for chord duration
        self.events += struct.pack(">BBB", 0x80, NOTE_MAP[notes[0]+oct], 0)
        for note in notes[1:]:
            note_num = NOTE_MAP[note + oct]
            self.events += encode_vlq(0)
            self.events += struct.pack(">BBB", 0x80, note_num, 0)  # Note-off, velocity 0
    
    def add_group(self, notelist, dur):  # notes in list encoded in same format as in add_note
        # First expand any chords in the notelist
        expanded_notes = []
        for n in notelist:
            if n.text[-1] == '*':  # Is a chord
                base, oct = n.text[:-2], n.text[-2]
                bases = CHORD_MAP[base]
                expanded_notes += [b+oct for b in bases]
            else:
                expanded_notes.append(n.text)

        notelist = expanded_notes

        self.events += encode_vlq(self.rest_ticks)  # Apply rest before playing the chord
        self.events += struct.pack(">BBB", 0x90, NOTE_MAP[notelist[0]], 64)
        for note in notelist[1:]:
            note_num = NOTE_MAP[note]
            self.events += encode_vlq(0)  # Same time as other notes
            self.events += struct.pack(">BBB", 0x90, note_num, 64)  # Note-on, velocity 64

        self.rest_ticks = 0

        self.events += encode_vlq(int(dur * self.tpq))  # Delta time for chord duration
        self.events += struct.pack(">BBB", 0x80, NOTE_MAP[notelist[0]], 0)
        for note in notelist[1:]:
            note_num = NOTE_MAP[note]
            self.events += encode_vlq(0)
            self.events += struct.pack(">BBB", 0x80, note_num, 0)  # Note-off, velocity 0

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

class MidiGenerator:
    def __init__(self, tempo, note_seq, dur_seq, tpq=480):
        self.header = HeaderChunk(tpq)
        self.track = TrackChunk(tpq)
        self.note_seq = note_seq
        self.dur_seq = dur_seq
        self.tempo = tempo
    
    def generate(self, fname):
        tempo_data = struct.pack(">I", int(60000000 / self.tempo))[1:]
        self.track.add_meta_event(0x51, tempo_data)

        skipped = []
        dur_ind = 0
        for num, note in enumerate(self.note_seq):
            if num in skipped:
                continue

            if not isinstance(note, int):
                self.track.add(note, self.dur_seq[dur_ind])
            else:  # is a group; value says number of notes to include
                cnt = note
                self.track.add_group(self.note_seq[num+1:num+1+cnt], self.dur_seq[num])
                skipped += [r for r in range(num+1, num+1+cnt)]
            dur_ind += 1

        self.track.end_track()

        with open(f'{fname}.mid', "wb") as midi:
            midi.write(self.header.bytes())
            midi.write(self.track.bytes())


# Note Map - Maps text notes from C1 to B7 (sharps specified as ex. C#1 and flats as ex. Cb1)
NOTE_MAP = {
    # Octave 1
    "C1": 12, "C#1": 13, "Db1": 13, "D1": 14, "D#1": 15, "Eb1": 15,
    "E1": 16, "F1": 17, "F#1": 18, "Gb1": 18, "G1": 19, "G#1": 20, "Ab1": 20,
    "A1": 21, "A#1": 22, "Bb1": 22, "B1": 23,
    # Octave 2
    "C2": 24, "C#2": 25, "Db2": 25, "D2": 26, "D#2": 27, "Eb2": 27,
    "E2": 28, "F2": 29, "F#2": 30, "Gb2": 30, "G2": 31, "G#2": 32, "Ab2": 32,
    "A2": 33, "A#2": 34, "Bb2": 34, "B2": 35,
    # Octave 3
    "C3": 36, "C#3": 37, "Db3": 37, "D3": 38, "D#3": 39, "Eb3": 39,
    "E3": 40, "F3": 41, "F#3": 42, "Gb3": 42, "G3": 43, "G#3": 44, "Ab3": 44,
    "A3": 45, "A#3": 46, "Bb3": 46, "B3": 47,
    # Octave 4
    "C4": 48, "C#4": 49, "Db4": 49, "D4": 50, "D#4": 51, "Eb4": 51,
    "E4": 52, "F4": 53, "F#4": 54, "Gb4": 54, "G4": 55, "G#4": 56, "Ab4": 56,
    "A4": 57, "A#4": 58, "Bb4": 58, "B4": 59,
    # Octave 5
    "C5": 60, "C#5": 61, "Db5": 61, "D5": 62, "D#5": 63, "Eb5": 63,
    "E5": 64, "F5": 65, "F#5": 66, "Gb5": 66, "G5": 67, "G#5": 68, "Ab5": 68,
    "A5": 69, "A#5": 70, "Bb5": 70, "B5": 71,
    # Octave 6
    "C6": 72, "C#6": 73, "Db6": 73, "D6": 74, "D#6": 75, "Eb6": 75,
    "E6": 76, "F6": 77, "F#6": 78, "Gb6": 78, "G6": 79, "G#6": 80, "Ab6": 80,
    "A6": 81, "A#6": 82, "Bb6": 82, "B6": 83,
    # Octave 7
    "C7": 84, "C#7": 85, "Db7": 85, "D7": 86, "D#7": 87, "Eb7": 87,
    "E7": 88, "F7": 89, "F#7": 90, "Gb7": 90, "G7": 91, "G#7": 92, "Ab7": 92,
    "A7": 93, "A#7": 94, "Bb7": 94, "B7": 95
}

# Chord Map - Maps chords to lists of notes from C1 to C5 (supports major and minor | Ex. C-sharp major = C#+ and C-flat minor = ex. Cb-)
CHORD_MAP = {
    "C+": ["C", "E", "G"],
    "C-": ["C", "Eb", "G"],
    "C#+": ["C#", "F", "G#"],
    "C#-": ["C#", "E", "G#"],
    "D+": ["D", "F#", "A"],
    "D-": ["D", "F", "A"],
    "D#+": ["D#", "G", "A#"],
    "D#-": ["D#", "F#", "A#"],
    "E+": ["E", "G#", "B"],
    "E-": ["E", "G", "B"],
    "F+": ["F", "A", "C"],
    "F-": ["F", "Ab", "C"],
    "F#+": ["F#", "A#", "C#"],
    "F#-": ["F#", "A", "C#"],
    "G+": ["G", "B", "D"],
    "G-": ["G", "Bb", "D"],
    "G#+": ["G#", "C", "D#"],
    "G#-": ["G#", "B", "D#"],
    "A+": ["A", "C#", "E"],
    "A-": ["A", "C", "E"],
    "A#+": ["A#", "D", "F"],
    "A#-": ["A#", "C#", "F"],
    "B+": ["B", "D#", "F#"],
    "B-": ["B", "D", "F#"]
}

# from parse import Token
# nseq = [Token('NOTE', 'F4'), Token('CHORD', 'C+5*'), 2, Token('CHORD', 'C+5*'), Token('NOTE', 'B5')]
# dseq = [1, 1, 3]
# tempo = 120

# gen = MidiGenerator(tempo, nseq, dseq)
# gen.generate('demo')