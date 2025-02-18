class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.non_terminals.union({"F"})  # Add final state "F"
        self.alphabet = grammar.terminals
        self.transitions = {state: {} for state in self.states}  # Initialize empty transitions
        self.start_state = grammar.start_symbol
        self.final_state = {"F"}
        self.__build_transitions(grammar)

    def __build_transitions(self, grammar):
        for non_terminal, production_list in grammar.productions.items():
            for production in production_list:
                current_state = non_terminal
                for symbol in production:
                    if symbol in grammar.terminals:
                        # Terminal transition
                        if symbol not in self.transitions[current_state]:
                            self.transitions[current_state][symbol] = []
                        result = "".join([c for c in production if c != symbol])
                        self.transitions[current_state][symbol].append(result if result != "" else "F")


    def display_transitions(self):
        print("Finite Automaton Transitions:")
        print(self.transitions)
        for state, transitions in self.transitions.items():
            for symbol, target_states in transitions.items():
                print(f"State {state} --({symbol})--> {target_states}")
