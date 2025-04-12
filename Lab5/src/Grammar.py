from itertools import chain, combinations

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.N_lambda = set()

    def eliminate_empty_productions(self):
        N_lambda = set()

        for nt, prods in self.productions.items():
            if "epsilon" in prods:
                N_lambda.add(nt)

        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in N_lambda:
                    continue

                for prod in prods:
                    if all(symbol in N_lambda for symbol in prod):
                        N_lambda.add(nt)
                        changed = True
                        break

        self.N_lambda = N_lambda
        print(f"Nullable non-terminals: {N_lambda}")

        new_productions = {nt: [] for nt in self.productions}

        for nt, prods in self.productions.items():
            for prod in prods:
                if prod == "epsilon":
                    continue

                nullable_indices = []
                for i, symbol in enumerate(prod):
                    if symbol in N_lambda:
                        nullable_indices.append(i)

                all_subsets = chain.from_iterable(combinations(nullable_indices, r)
                                                  for r in range(len(nullable_indices) + 1))

                for subset in all_subsets:
                    new_prod = "".join(symbol for i, symbol in enumerate(prod) if i not in subset)

                    if new_prod and new_prod not in new_productions[nt]:
                        new_productions[nt].append(new_prod)

        self.productions = new_productions
        print(self.productions)
        return self



