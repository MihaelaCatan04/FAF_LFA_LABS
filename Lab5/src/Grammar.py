class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.N_lambda = set()

    def eliminate_empty_productions(self):
        changed = True
        while changed:
            changed = False
            for x, prods in self.productions.items():
                for prod in prods:
                    if prod == "epsilon" or all(
                            symbol in self.N_lambda for symbol in prod if symbol in self.non_terminals):
                        if x not in self.N_lambda:
                            self.N_lambda.add(x)
                            changed = True
        new_productions = {}
        for x, prods in self.productions.items():
            new_productions[x] = []
            for prod in prods:
                if prod != "epsilon":
                    new_productions[x].append(prod)
                # Generate all possible variations by removing nullable non-terminals




