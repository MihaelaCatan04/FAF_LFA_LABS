import Grammar
grammar = Grammar.Grammar({"S", "I", "J", "K"}, {"a", "b", "c", "e", "n", "f", "m"}, {
            'S': ['cI'],
            'I': ['bJ', 'fI', 'e', 'eK'],
            'J': ['nJ', 'cS'],
            'K': ['nK', 'm']
        }, "S")

print(grammar.return_grammar_type())