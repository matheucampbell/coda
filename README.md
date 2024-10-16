# coda
Compiler for Coda MIDI description language

## Installation

## Lexical Specification
### Tokens
**Note** - ['A'-'G']['#', 'b']?[1-7] \
**Key** - ['A'-'G']['#', 'b']?['-', '+'] \
**Chord** - ['A'-'G'][#, b]?['-', '+'][1-7]['Ch'] \
**Declarator** - ['!'] \
**Keyword** - ['key', 'sig', 'typ', 'rep', 'grp'] \
**Separator** - [','] \
**Connector** - ['>']['>']? \
**Lbrace** - ['{'] \
**Rbrace** - ['}'] \
**Lbracket** - ['['] \
**Rbracket** - [']'] \
**Separator** - [','] \
**Comment** - ['//']['A'-'Z''a'-'z']*['\n']