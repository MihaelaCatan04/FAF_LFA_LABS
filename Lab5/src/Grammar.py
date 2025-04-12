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

    def eliminate_unit_productions(self):
        unit_pairs = {}
        for nt in self.non_terminals:
            unit_pairs[nt] = {nt}

        changed = True
        while changed:
            changed = False
            for a in self.non_terminals:
                for prod in self.productions.get(a, []):
                    if prod in self.non_terminals:
                        for b in unit_pairs.get(prod, set()):
                            if b not in unit_pairs[a]:
                                unit_pairs[a].add(b)
                                changed = True

        new_productions = {nt: [] for nt in self.non_terminals}

        for a in self.non_terminals:
            for b in unit_pairs[a]:
                for prod in self.productions.get(b, []):
                    if prod not in self.non_terminals and prod not in new_productions[a]:
                        new_productions[a].append(prod)

        self.productions = new_productions
        print(self.productions)
        return self

    def eliminate_non_productive_symbols(self):
        productive = set()

        for nt, prods in self.productions.items():
            for prod in prods:
                if all(symbol in self.terminals for symbol in prod):
                    productive.add(nt)
                    break

        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in productive:
                    continue

                for prod in prods:
                    if all(symbol in self.terminals or symbol in productive for symbol in prod):
                        productive.add(nt)
                        changed = True
                        break

        new_non_terminals = {nt for nt in self.non_terminals if nt in productive}
        new_productions = {}

        for nt in new_non_terminals:
            new_productions[nt] = [prod for prod in self.productions.get(nt, [])
                                   if all(symbol not in self.non_terminals or symbol in productive
                                          for symbol in prod)]

        self.non_terminals = new_non_terminals
        self.productions = new_productions
        print(self.productions)
        return self

    def eliminate_inaccessible_symbols(self):
        accessible = {self.start_symbol}
        queue = [self.start_symbol]

        while queue:
            current = queue.pop(0)
            for prod in self.productions.get(current, []):
                for symbol in prod:
                    if symbol in self.non_terminals and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        new_non_terminals = {nt for nt in self.non_terminals if nt in accessible}
        new_productions = {}

        for nt in new_non_terminals:
            new_productions[nt] = [prod for prod in self.productions.get(nt, [])
                                   if all(symbol not in self.non_terminals or symbol in accessible
                                          for symbol in prod)]

        self.non_terminals = new_non_terminals
        self.productions = new_productions
        print(self.productions)
        return self

