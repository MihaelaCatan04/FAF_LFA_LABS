import random

from blinker._utilities import symbol


class Grammar:
    # Initialize the Grammar class with non-terminals, terminals, productions, and start symbol
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals  # Non-terminal symbols (e.g., variables like S, A, B)
        self.terminals = terminals  # Terminal symbols (e.g., actual characters or tokens)
        self.productions = productions  # Dictionary of productions for each non-terminal
        self.start_symbols = start_symbol  # The starting non-terminal for generating strings

    # Method to generate a string based on the grammar rules
    def generate_string(self):
        # Randomly select a production for the start symbol and initialize the result
        result = random.choice(self.productions[self.start_symbols])

        # Continue replacing non-terminals with their respective productions until there are no non-terminals left
        while any(non_terminal in result for non_terminal in self.non_terminals):
            final_result = ""
            for letter in result:
                if letter in self.non_terminals:
                    # Replace non-terminals with random productions
                    final_result += random.choice(self.productions[letter])
                else:
                    # Keep terminal symbols as they are
                    final_result += letter
            # Update the result with the new expanded string
            result = final_result

        return result

    # Method to generate a list of strings (multiple generations)
    def generate_strings(self, number_of_strings):
        strings = []
        for _ in range(number_of_strings):
            # Generate and append each string to the list
            strings.append(self.generate_string())
        return strings

    # Check if the grammar is of Type 3 (Regular grammar)
    def __check_type3(self):
        type3 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals and len(non_terminal) == 1:
                for prod in production:
                    # Check production rules for Type 3 grammar (either single terminal or terminal followed by non-terminal)
                    if len(prod) == 1 and prod in self.terminals:
                        continue
                    elif len(prod) == 2 and prod[0] in self.terminals and prod[1] in self.non_terminals:
                        continue
                    elif len(prod) == 2 and prod[0] in self.non_terminals and prod[1] in self.terminals:
                        continue
                    else:
                        type3 = False
                        break
            else:
                type3 = False
                break
        return type3

    # Check if the grammar is of Type 2 (Context-free grammar)
    def __check_type2(self):
        type2 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals and len(non_terminal) == 1:
                for prod in production:
                    # Check if the production is valid for a Type 2 grammar
                    if len(prod) == 0 or all(
                            symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                        continue
                    else:
                        type2 = False
                        break
            else:
                type2 = False
                break
        return type2

    # Check if the grammar is of Type 1 (Context-sensitive grammar)
    def __check_type1(self):
        type1 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals:
                for prod in production:
                    # Check if production is valid for Type 1 grammar (productions must follow specific rules)
                    if len(non_terminal) <= len(prod) and all(
                            symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                        continue
                    else:
                        type1 = False
                        break
            else:
                type1 = False
                break
        return type1

    # Check if the grammar is of Type 0 (Unrestricted grammar)
    def __check_type0(self):
        type0 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals:
                for prod in production:
                    # Type 0 allows unrestricted production rules
                    if all(symbol in self.terminals or symbol in self.non_terminals for symbol in prod) or len(
                            prod) == 0:
                        continue
                    else:
                        type0 = False
                        break
            else:
                type0 = False
                break
        return type0

    # Determine the type of grammar (Type 3, 2, 1, 0 or Invalid)
    def return_grammar_type(self):
        # Check for Type 0, then Type 1, Type 2, and Type 3 in sequence
        if self.__check_type0():
            if self.__check_type1():
                if self.__check_type2():
                    if self.__check_type3():
                        return "Grammar Type 3"
                    else:
                        return "Grammar Type 2"
                else:
                    return "Grammar Type 1"
            else:
                return "Grammar Type 0"
        else:
            return "Invalid Grammar Type"
