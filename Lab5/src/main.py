import Grammar
grammar = Grammar.Grammar({"S", "A", "B", "C", "E"}, {"a", "b"}, {
            'S': ['aB', 'AC'],
            'A': ['a', 'ASC', 'BC'],
            'B': ['b', 'bS'],
            'C': ['epsilon', 'BA'],
            'E': ['bB'],
        }, "S")
grammar.eliminate_empty_productions()
grammar.eliminate_unit_productions()
grammar.eliminate_non_productive_symbols()