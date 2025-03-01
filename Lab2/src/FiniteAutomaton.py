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
    def visualize(self):
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
        dot.render('finite_automaton', format='png', view=True)
