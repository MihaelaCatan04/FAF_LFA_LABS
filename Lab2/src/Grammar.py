class Grammar(object):
    # Initialize the Grammar class with non-terminals, terminals, productions, and the start symbol
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        # Non-terminal symbols
        self.non_terminals = non_terminals
        # Terminal symbols
        self.terminals = terminals
        # Dictionary of productions for each non-terminal
        self.productions = productions
        # The starting non-terminal for generating strings
        self.start_symbols = start_symbol

    # Method to print the grammar in a readable format
    def print_grammar(self):
        print("Grammar:")
        print(f"Start Symbol: {self.start_symbols}")
        print("Non-Terminals:", ", ".join(self.non_terminals))
        print("Terminals:", ", ".join(self.terminals))
        print("Productions:")
        print(self.productions)
