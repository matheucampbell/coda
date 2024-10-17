## Contributors
Matheu Campbell (mgc2171)

## Installation

## Lexical Specification
### Tokens
**Note** - A single musical note \
['A'-'G']['#', 'b']?[1-7] \
**Key** - Key signature of the following block \
['A'-'G']['#', 'b']?['-', '+'] \
**Chord** - A triad, specified with root note, accidental, octave, and quality\
['A'-'G'][#, b]?['-', '+'][1-7]['\*'] \
**Declarator** - Marks the next keyword to be applied globally \
['!'] \
**Keyword** - Specify key, time signature, note type, repetitions, or groupings of notes \
['key', 'sig', 'typ', 'rep', 'grp'] \
**Separator** - Separator keyword arguments \
[','] \
**Connector** - Specifies standard or legato articulation between adjacent notes and chords \
['>']['>']? \
**Lbrace** - Marks beginning of block \
['{'] \
**Rbrace** - Marks end of block \
['}'] \
**Lbracket** - Encloses keyword arguments \
['['] \
**Rbracket** - Encloses keyword arguments \
[']'] \
**Comment** - Text ignored by compiler \
['//']~['\n']\*['\n']