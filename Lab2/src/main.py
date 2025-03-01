from Lab2.src import FiniteAutomaton

states = {"q0", "q1", "q2", "q3", "q4"}
alphabet = {"a", "b"}
transitions = [
    {"state": "q0", "symbol": "a", "to": "q1"},
    {"state": "q1", "symbol": "b", "to": "q1"},
    {"state": "q1", "symbol": "b", "to": "q2"},
    {"state": "q2", "symbol": "b", "to": "q3"},
    {"state": "q3", "symbol": "a", "to": "q1"},
    {"state": "q2", "symbol": "a", "to": "q4"},
]
initial_state = "q0"
final_state = {"q4"}

finite_automaton = FiniteAutomaton.FiniteAutomaton(states, alphabet, initial_state, final_state, transitions)
print(finite_automaton.is_deterministic())
print(finite_automaton.convert_to_grammar().print_grammar())
finite_automaton.visualize()

