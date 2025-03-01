class Grammar(object):
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbols = start_symbol

    def print_grammar(self):
        print("Grammar:")
        print(f"Start Symbol: {self.start_symbols}")

        # Print Non-Terminals
        print("Non-Terminals:", ", ".join(self.non_terminals))

        # Print Terminals
        print("Terminals:", ", ".join(self.terminals))

        # Print Productions
        print("Productions:")
        print(self.productions)
