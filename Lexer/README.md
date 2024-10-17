## Contributors
Matheu Campbell (mgc2171)

## Installation/Build Steps
1. Install Docker for the appropriate operating system.
   The lexer uses for packaging/containerization.
2. Navigate to the Lexer subdirectory of this repository.
3. Run `docker build -t coda-lexer .` to build the Docker image.

## Execution Steps
To run the lexer on an input file after building in this directory, run
`docker run --rm -v "$(pwd)"/<INPUT_FILE>:/app/<INPUT_FILE> coda-lexer -i <INPUT_FILE>`

To run the lexer on the Examples in this folder, provide their paths as input files. Make sure to include `/Examples/` in the -v argument if running directly from this directory. For example, to run the first demo, run `docker run --rm -v "$(pwd)"/Examples/codalex_demo1.cd:/app/codalex_demo1.cd coda-lexer -i codalex_demo1.cd`

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