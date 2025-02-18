import random


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
