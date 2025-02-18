import random


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        result = random.choice(self.productions[self.start_symbol])
        while any(non_terminal in result for non_terminal in self.non_terminals):
            final_result = ""
            for letter in result:
                if letter in self.non_terminals:
                    final_result += random.choice(self.productions[letter])
                else:
                    final_result += letter
            result = final_result
        return result

    def generate_strings(self, number_of_strings):
        strings = []
        for _ in range(number_of_strings):
            strings.append(self.generate_string())
        return strings
