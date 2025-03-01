import random

from blinker._utilities import symbol


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbols = start_symbol

    # Method to generate a string
    def generate_string(self):
        # Randomly select an initial production from the start symbol's productions
        result = random.choice(self.productions[self.start_symbols])
        # Continue generating the string until there are no non-terminals left in the result
        while any(non_terminal in result for non_terminal in self.non_terminals):
            # Initialize a new string to hold the final result
            final_result = ""
            # Iterate over each character in the current result
            for letter in result:
                if letter in self.non_terminals:
                    # If the character is a non-terminal, replace it with a random production for that non-terminal
                    final_result += random.choice(self.productions[letter])
                else:
                    # If the character is a terminal, keep it unchanged
                    final_result += letter
            # Update the result with the newly expanded string
            result = final_result
        return result

    # Method to generate a list of strings
    def generate_strings(self, number_of_strings):
        strings = []
        for _ in range(number_of_strings):
            strings.append(self.generate_string())
        return strings

    def __check_type3(self):
        type3 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals and len(non_terminal) == 1:
                for prod in production:
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

    def __check_type2(self):
        type2 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals and len(non_terminal) == 1:
                for prod in production:
                    if len(prod) == 0 or all(symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                        continue
                    else:
                        type2 = False
                        break
            else:
                type2 = False
                break
        return type2

    def __check_type1(self):
        type1 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals:
                for prod in production:
                    if len(non_terminal) <= len(prod) and all(symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                        continue
                    else:
                        type1 = False
                        break
            else:
                type1 = False
                break
        return type1

    def __check_type0(self):
        type0 = True
        for non_terminal, production in self.productions.items():
            if non_terminal in self.non_terminals:
                for prod in production:
                    if all(symbol in self.terminals or symbol in self.non_terminals for symbol in prod) or len(prod) == 0:
                        continue
                    else:
                        type0 = False
                        break
            else:
                type0 = False
                break
        return type0




    def return_grammar_type(self):
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

