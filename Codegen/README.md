## Contributors
Matheu Campbell (mgc2171)

## Installation/Build Steps
1. Install Docker for the appropriate operating system.
   The parser uses Docker for packaging/containerization.
2. Navigate to the Parser subdirectory of this repository.
3. Run `docker build -t coda-codegen .` to build the Docker image.

## Execution Steps
To run the lexer and parser on an input file after building in this directory, run
`docker run --rm -v "$(pwd)"/<INPUT_FILE>:/app/<INPUT_FILE> coda-codegen -i <INPUT_FILE>`
