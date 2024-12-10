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

## Language Features