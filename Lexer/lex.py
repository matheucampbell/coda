from codalexer import Lexer, Regex

note_stages = {
    0: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    1: ['#', 'b'],
    2: ['1', '2', '3', '4', '5', '6', '7']
}
note_opts = [1]
key_stages = {
    0: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    1: ['#', 'b'],
    2: ['-', '+']
}
key_opts = [1]
chord_stages = {
    0: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    1: ['#', 'b'],
    2: ['-', '+'],
    3: ['1', '2', '3', '4', '5', '6', '7'],
    4: ['*']
}
chord_opts = [1]
num_stages = {
    0: ['1', '2', '3', '4', '5', '6', '7', '8', '9']
}
comment_stages = {0: '/', 1: '/', 2: '\n', 3: '\n'}
comment_reps = [2]
comment_invs = [2]
kw_key_stages = {0: 'k', 1: 'e', 2: 'y'}
kw_sig_stages = {0: 's', 1: 'i', 2: 'g'}
kw_typ_stages = {0: 't', 1: 'y', 2: 'p'}
kw_rep_stages = {0: 'r', 1: 'e', 2: 'p'}
kw_grp_stages = {0: 'g', 1: 'r', 2: 'p'}
declarator_stages = {0: '!'}
separator_stages = {0: ','}
connector_stages = {0: '>', 1: '>'}
connector_opts = [1]
lbrace_stages = {0: '{'}
rbrace_stages = {0: '}'}
lbracket_stages = {0: '['}
rbracket_stages = {0: ']'}

lexer = Lexer()
lexer.register_token(Regex('NOTE', "['A'-'G']['#', 'b']?[1-7]",
                           note_stages,
                           optionals=note_opts))
lexer.register_token(Regex('KEY', "['A'-'G']['#', 'b']?['-', '+']?", 
                           key_stages, 
                           optionals=key_opts))
lexer.register_token(Regex('CHORD', "['A'-'G']['#', 'b']?[1-7]", 
                           chord_stages, 
                           optionals=chord_opts))
lexer.register_token(Regex('CONNECTOR', "['>']['>']?", 
                           connector_stages, 
                           optionals=connector_opts))
lexer.register_token(Regex('COMMENT', "['//']['A'-'Z''a'-'z']*['\n']", comment_stages,
                           repeats=comment_reps,
                           inverts=comment_invs))
lexer.register_token(Regex('DECLARATOR', "'!'", declarator_stages))
lexer.register_token(Regex('SEPARATOR', "','", separator_stages))
lexer.register_token(Regex('LBRACE', "'{'", lbrace_stages))
lexer.register_token(Regex('RBRACE', "'}'", rbrace_stages))
lexer.register_token(Regex('LBRACKET', "'['", lbracket_stages))
lexer.register_token(Regex('RBRACKET', "']'", rbracket_stages))
lexer.register_token(Regex('NUMBER', "['1'-'9']", num_stages))
lexer.register_token(Regex('KEYWORD', "['key']", kw_key_stages))
lexer.register_token(Regex('KEYWORD', "['sig']", kw_sig_stages))
lexer.register_token(Regex('KEYWORD', "['typ']", kw_typ_stages))
lexer.register_token(Regex('KEYWORD', "['rep']", kw_rep_stages))
lexer.register_token(Regex('KEYWORD', "['grp']", kw_grp_stages))

fpath = 'coda_sample1.cd'
lexer.tokenize(fpath)

for x in lexer.get_tokens():
    print(x)
