# coda
Compiler for Coda MIDI description language

## Installation

## Lexical Specification
### Tokens
**Note** - ['A'-'F']['#', 'b']?[1-7] \
**Key** - ['A'-'F']['#', 'b']?['-', '+'] \
**Chord** - ['A'-'F'][#, b]?['-', '+'][1-7]['Ch'] \
**Declarator** - ['!'] \
**Keyword** - ['key', 'sig', 'typ', 'rep', 'grp'] \
**Separator** - [','] \
**Connector** - ['>']['>']? \
**Lbrace** - ['{'] \
**Rbrace** - ['}'] \
**Lbracket** - ['['] \
**Rbracket** - [']'] \
**Separator** - [','] \
**Comment** - ['\\']['A'-'Z''a'-'z']*['\n']