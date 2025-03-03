from Lab2.src.Grammar import Grammar
from graphviz import Digraph


class FiniteAutomaton:
    # Initialize the FiniteAutomaton class with states, alphabet, initial state, final states, and transitions
    def __init__(self, states, alphabet, initial_state, final_state, transitions):
        # List of states in the automaton
        self.states = states
        # List of symbols in the alphabet (input symbols)
        self.alphabet = alphabet
        # The initial state of the automaton
        self.initial_state = initial_state
        # List of final (accepting) states
        self.final_state = final_state
        # List of transitions between states (e.g., state to state on input symbol)
        self.transitions = transitions

    # Check if the automaton is deterministic
    def is_deterministic(self):
        is_deterministic = True
        # Keep track of seen state-symbol pairs
        seen = []
        for transition in self.transitions:
            # Key is a pair of state and symbol
            key = [transition["state"], transition["symbol"]]
            if key in seen:
                # If the pair is seen again, it means it's non-deterministic
                is_deterministic = False
                break
            seen.append(key)
        return is_deterministic

    # Generate the productions for a context-free grammar from the automaton's transitions
    def __get_productions(self):
        # Dictionary to store productions for each state
        productions = {}
        # Initialize empty lists for each state in the automaton
        for transition in self.transitions:
            if transition["state"] not in productions:
                productions[transition["state"]] = []

        # Add the corresponding production rule for each transition
        for transition in self.transitions:
            # If the transition leads to a final state, add the symbol only
            if transition["to"] not in self.final_state:
                productions[transition["state"]].append(transition["symbol"] + transition["to"])
            else:
                # Otherwise, append the symbol
                productions[transition["state"]].append(transition["symbol"])
        return productions

    # Convert the finite automaton to a context-free grammar
    def convert_to_grammar(self):
        # States become non-terminals in the grammar
        non_terminals = self.states
        # Alphabet becomes terminals in the grammar
        terminals = self.alphabet
        # The initial state remains the same
        initial_state = self.initial_state
        # Get the productions from the transitions
        productions = self.__get_productions()
        # Create Grammar object
        grammar = Grammar(non_terminals, terminals, productions, initial_state)
        return grammar

    # Visualize the finite automaton using Graphviz
    def visualize(self, name):
        # Initialize the Graphviz Digraph object
        dot = Digraph(comment='Finite Automaton')

        # Add nodes (states) to the graph
        for state in self.states:
            if state == self.initial_state:
                # The initial state is represented with a dashed double circle
                dot.node(state, shape='doublecircle', style='dashed')
            elif state in self.final_state:
                # Final states are represented with a double circle
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        # Add edges (transitions) between states
        for transition in self.transitions:
            dot.edge(transition["state"], transition["to"], label=transition["symbol"])

        # Render the graph to a file and view it
        dot.render(name, format='png', view=True)

    # Convert an NDFA to a DFA
    def convert_to_dfa(self):
        # If the automaton is already deterministic, return it as is
        if self.is_deterministic():
            return self

        # Get the epsilon closure for a set of states
        def epsilon_closure(states):
            closure = set(states)
            stack = list(states)

            while stack:
                state = stack.pop()
                for transition in self.transitions:
                    if transition["state"] == state and transition["symbol"] == "":
                        if transition["to"] not in closure:
                            closure.add(transition["to"])
                            stack.append(transition["to"])
            return closure

        # Get the next states for a given set of states and input symbol
        def move(states, symbol):
            result = set()
            for state in states:
                for transition in self.transitions:
                    if transition["state"] == state and transition["symbol"] == symbol:
                        result.add(transition["to"])
            return result

        # Start with the epsilon closure of the initial state
        initial_dfa_state = frozenset(epsilon_closure({self.initial_state}))

        # Initialize DFA states and transitions
        dfa_states = [initial_dfa_state]
        dfa_transitions = []
        unprocessed_states = [initial_dfa_state]

        # Map of DFA states (which are sets of NDFA states) to state names
        state_mapping = {initial_dfa_state: "q0"}

        # Process all unprocessed DFA states
        while unprocessed_states:
            current_state_set = unprocessed_states.pop(0)

            # For each input symbol
            for symbol in self.alphabet:
                if symbol == "":  # Skip epsilon transitions in the DFA
                    continue

                # Get the next state set
                next_states = move(current_state_set, symbol)
                next_state_closure = frozenset(epsilon_closure(next_states))

                # If this is a new state, add it to the list of states to process
                if next_state_closure and next_state_closure not in dfa_states:
                    dfa_states.append(next_state_closure)
                    unprocessed_states.append(next_state_closure)
                    state_mapping[next_state_closure] = f"q{len(state_mapping)}"

                # Add the transition if the next state set is not empty
                if next_state_closure:
                    dfa_transitions.append({
                        "state": state_mapping[current_state_set],
                        "symbol": symbol,
                        "to": state_mapping[next_state_closure]
                    })

        # Determine the final states of the DFA
        dfa_final_states = []
        for dfa_state_set in dfa_states:
            # If any NDFA state in this set is a final state, the DFA state is final
            if any(state in self.final_state for state in dfa_state_set):
                dfa_final_states.append(state_mapping[dfa_state_set])

        # Create list of state names for the DFA
        dfa_state_names = list(state_mapping.values())

        # Create the new DFA
        dfa = FiniteAutomaton(
            states=dfa_state_names,
            alphabet=[symbol for symbol in self.alphabet if symbol != ""],  # Remove epsilon
            initial_state="q0",
            final_state=dfa_final_states,
            transitions=dfa_transitions
        )

        return dfa

