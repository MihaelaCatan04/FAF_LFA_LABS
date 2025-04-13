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
        original_start = None
        special_start = None
        if self.start_symbol.endswith("'"):
            special_start = self.start_symbol
            original_start = self.start_symbol.rstrip("'")

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

        if special_start and original_start:
            new_productions[special_start] = [original_start]

        for a in self.non_terminals:
            if a == special_start:
                continue

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

    def convert_long_productions(self):
        new_productions = {}
        new_non_terminals = set(self.non_terminals)
        next_nt_index = 1

        for nt, prods in self.productions.items():
            new_productions[nt] = []

            for prod in prods:
                if len(prod) <= 2:
                    new_productions[nt].append(prod)
                else:
                    symbols = list(prod)
                    current_nt = nt

                    while len(symbols) > 2:
                        first = symbols.pop(0)

                        new_nt = f"Y{next_nt_index}"
                        next_nt_index += 1
                        new_non_terminals.add(new_nt)

                        new_productions.setdefault(current_nt, []).append(first + new_nt)

                        current_nt = new_nt

                    new_productions.setdefault(current_nt, []).append("".join(symbols))

        self.non_terminals = new_non_terminals
        self.productions = new_productions
        print(self.productions)
        return self

    def convert_terminal_productions(self):
        new_productions = {}
        new_non_terminals = set(self.non_terminals)
        terminal_nts = {}

        for terminal in self.terminals:
            terminal_nt = f"X_{terminal}"
            new_non_terminals.add(terminal_nt)
            new_productions[terminal_nt] = [terminal]
            terminal_nts[terminal] = terminal_nt

        for nt, prods in self.productions.items():
            new_productions.setdefault(nt, [])

            for prod in prods:
                if len(prod) == 1:
                    new_productions[nt].append(prod)
                else:
                    new_prod = ""
                    for symbol in prod:
                        if symbol in self.terminals:
                            new_prod += terminal_nts[symbol]
                        else:
                            new_prod += symbol
                    new_productions[nt].append(new_prod)

        self.non_terminals = new_non_terminals
        self.productions = new_productions
        print(self.productions)
        return self

    def convert_to_chomsky_form(self):
        print("Starting conversion to Chomsky Normal Form...")

        new_start_needed = False
        for nt, prods in self.productions.items():
            for prod in prods:
                if self.start_symbol in prod:
                    new_start_needed = True
                    print(f"Start symbol '{self.start_symbol}' appears in a production of '{nt}', new start needed.")
                    break
            if new_start_needed:
                break

        if new_start_needed:
            new_start = f"{self.start_symbol}'"
            while new_start in self.non_terminals:
                new_start += "'"
            print(f"Creating new start symbol: {new_start}")

            self.non_terminals.add(new_start)
            self.productions[new_start] = [self.start_symbol]
            self.start_symbol = new_start
            print(
                f"Updated start symbol to '{self.start_symbol}'. Added production: {new_start} -> {self.productions[new_start]}")

        print("Eliminating empty productions...")
        self.eliminate_empty_productions()
        print("Empty productions eliminated.")

        print("Eliminating unit productions...")
        self.eliminate_unit_productions()
        print("Unit productions eliminated.")

        print("Eliminating inaccessible symbols...")
        self.eliminate_inaccessible_symbols()
        print("Inaccessible symbols eliminated.")

        print("Eliminating non-productive symbols...")
        self.eliminate_non_productive_symbols()
        print("Non-productive symbols eliminated.")

        print("Converting long productions to binary...")
        self.convert_long_productions()
        print("Long productions converted.")

        print("Converting terminals in productions with length > 1...")
        self.convert_terminal_productions()
        print("Terminal productions converted.")

        print("Conversion to Chomsky Normal Form completed.\n")
        print(self.productions)
        return self


