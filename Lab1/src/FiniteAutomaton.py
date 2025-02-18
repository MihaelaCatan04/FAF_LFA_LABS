from collections import deque

class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.non_terminals.union({"F"})
        self.alphabet = grammar.terminals
        self.transitions = {state: {} for state in self.states}
        self.start_state = grammar.start_symbols
        self.final_states = {"F"}
        self.__build_transitions(grammar)

    # Method for creating transitions from productions
    def __build_transitions(self, grammar):
        # Iterate over each non-terminal and its corresponding list of productions
        for non_terminal, production_list in grammar.productions.items():
            # For each production, iterate through its symbols to identify terminals and handle transitions
            for production in production_list:
                current_state = non_terminal
                for symbol in production:
                    if symbol in grammar.terminals:
                        # Create or update transitions for each terminal symbol in the production
                        if symbol not in self.transitions[current_state]:
                            # Initialize the list for the terminal symbol if it does not already have any transitions
                            self.transitions[current_state][symbol] = []
                        # Determine the resulting state by removing the current terminal from the production
                        # If the result is empty, transition to the final state 'F'
                        result = "".join([c for c in production if c != symbol])
                        self.transitions[current_state][symbol].append(result if result != "" else "F")

    # Method do display the transitions
    def display_transitions(self):
        print("Finite Automaton Transitions:")
        print(self.transitions)
        for state, transitions in self.transitions.items():
            for symbol, target_states in transitions.items():
                print(f"State {state} --({symbol})--> {target_states}")

    # Method to check if a string can be obtained via the state transition
    def check_string(self, given_input):
        # Initialize a deque to store (state, index) pairs for traversal
        queue = deque([(self.start_state, 0)])
        # Process the queue until all possible paths are explored
        while queue:
            # Dequeue the current state and the current index in the input string
            current_state, index = queue.popleft()
            # Check if the end of the input string has been reached
            if index == len(given_input):
                # Check if the state is in the final states
                if current_state in self.final_states:
                    return True
                # Otherwise, continue exploring other transitions
                continue
            # Get the current symbol from the input string
            symbol = given_input[index]
            # Check if there are transitions from the current state for the given symbol
            if symbol in self.transitions.get(current_state):
                # Enqueue all possible next states along with the incremented index
                for next_state in self.transitions[current_state][symbol]:
                    queue.append((next_state, index + 1))
        # If no valid transition reaches a final state, the string is rejected
        return False
