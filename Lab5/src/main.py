import Grammar
grammar = Grammar.Grammar({"S", "A", "B", "C", "E"}, {"a", "b"}, {
            'S': ['aB', 'AC'],
            'A': ['a', 'ASC', 'BC'],
            'B': ['b', 'bS'],
            'C': ['epsilon', 'BA'],
            'E': ['bB'],
        }, "S")
grammar.convert_to_chomsky_form()