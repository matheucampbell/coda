## Contributors
Matheu Campbell (mgc2171)

## Installation/Build Steps
1. Install Docker for the appropriate operating system.
   The parser uses Docker for packaging/containerization.
2. Navigate to the Parser subdirectory of this repository.
3. Run `docker build -t coda .` to build the Docker image.

## Execution Steps
To fully compile a Coda program on an input file after building in this directory, run `docker run --rm -v "$(pwd)"/<INPUT_FILE>:/app/<INPUT_FILE> coda -i <INPUT_FILE> -o <OUTPUT_FILENAME>`

To run the parser on the Examples in this folder, provide their paths as input files. Make sure to include `/Examples/` in the -v argument if running directly from this directory. For example, to run the first demo, run `docker run --rm -v "$(pwd)"/Examples/codademo1.cd.cd:/app/coda_demo1.cd coda -i codaparse_demo1.cd -o output.mid`

## Structure
Coda encodes music to be directly converted to .midi files. A Coda consists of a header with required global identifiers followed by any number of note blocks, each having their own local modifiers. The blocks are nestable, allowing users to encode complex structures without excessive repetition.

### Global modifiers
!key[keysig] - specifies the key signature of the piece
!tmp[tempo] - specifies the tempo of the piece
!sig[timesig] - specifies the time signature of the piece

### Local modifiers
typ[n] - specifies the duration of the notes in the following block (inherited by all inner blocks unless redefined)
rep[n] - declares the following block to be repeated n times
grp[n] - decalres the following block to be played all at once

### Note and Chord Specifiers
Notes, chords, keys, and groups are specified according to the README found in the lexing section. 

## Optimizations
Coda correctly processes groups of notes larger than 3 which are not standard major/minor triads into chord structures and expands them automatically, allowing user flexibility and efficient execution.