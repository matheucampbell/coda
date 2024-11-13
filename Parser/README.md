## Contributors
Matheu Campbell (mgc2171)

## Installation/Build Steps
1. Install Docker for the appropriate operating system.
   The lexer uses Docker for packaging/containerization.
2. Navigate to the Lexer subdirectory of this repository.
3. Run `docker build -t coda-parser .` to build the Docker image.

## Execution Steps
To run the lexer and parser on an input file after building in this directory, run
`docker run --rm -v "$(pwd)"/<INPUT_FILE>:/app/<INPUT_FILE> coda-parser -i <INPUT_FILE>`

To run the parser on the Examples in this folder, provide their paths as input files. Make sure to include `/Examples/` in the -v argument if running directly from this directory. For example, to run the first demo, run `docker run --rm -v "$(pwd)"/Examples/codalex_demo1.cd:/app/codaparse_demo1.cd coda-parser -i codaparse_demo1.cd`

## Coda - Contex Free Grammar Specification
A coda program consists of sequences of notes that may or may not be encapsulated in blocks, signified by curly braces.
The author can specify properties of the notes within blocks using modifiers, which change the duration of enclosed notes (typ),
the number of times the enclosed block should be repeated (rep), and how many of the notes should be grouped and played at once (grp).
In addition to block modifiers, there are three mandatory glibal modifiers to be included before any notes or blocks are defined. These are the
key signature, tempo, and time signature modifiers, and they apply to the entire coda sheet.

The structure is captured in the following context-free grammar, with starting symbol `S`.

```
Tokens
note | chord | rest | keysig | number | key | sig | tmp | typ | rep | grp | ! | , | > | >> | { | } [ | ]

S -> IB
I -> !K!M!D
K -> key[keysig]
M -> sig[number, number]
D -> tmp[number]
B -> CB'
B'-> CB' | eps
C -> TRG{B} | N
T -> typ[number] | eps
R -> rep[number] | eps
G -> grp[number] | eps
N -> WN'
N'-> >N | >>N | eps
W -> chord | note | rest
````