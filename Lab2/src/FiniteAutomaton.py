from Lab2.src.Grammar import Grammar
from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self, states, alphabet, initial_state, final_state, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_state = final_state
        self.transitions = transitions

    def is_deterministic(self):
        is_deterministic = True
        seen = []
        for transition in self.transitions:
            key = [transition["state"], transition["symbol"]]
            if key in seen:
                is_deterministic = False
                break
            seen.append(key)
        return is_deterministic

    def __get_productions(self):
        productions = {}
        for transition in self.transitions:
            if transition["state"] not in productions:
                productions[transition["state"]] = []

        for transition in self.transitions:
            if transition["to"] not in self.final_state:
                productions[transition["state"]].append(transition["symbol"] + transition["to"])
            else:
                productions[transition["state"]].append(transition["symbol"])
        return productions

    def convert_to_grammar(self):
        non_terminals = self.states
        terminals = self.alphabet
        initial_state = self.initial_state
        productions = self.__get_productions()
        grammar = Grammar(non_terminals, terminals, productions, initial_state)
        return grammar

    def visualize(self):
        dot = Digraph(comment='Finite Automaton')

        for state in self.states:
            if state == self.initial_state:
                dot.node(state, shape='doublecircle', style='dashed')
            elif state in self.final_state:
                dot.node(state, shape='doublecircle')
                dot.node(state)

        for transition in self.transitions:
            dot.edge(transition["state"], transition["to"], label=transition["symbol"])

        dot.render('finite_automaton', format='png', view=True)
