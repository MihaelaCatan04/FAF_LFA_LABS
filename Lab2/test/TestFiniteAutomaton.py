import unittest
from Lab2.src.FiniteAutomaton import FiniteAutomaton


class TestFiniteAutomaton(unittest.TestCase):

    def setUp(self):
        self.states = {"q0", "q1", "q2", "q3", "q4"}
        self.alphabet = {"a", "b"}
        self.initial_state = "q0"
        self.final_state = {"q4"}
        self.transitions = [
            {"state": "q0", "symbol": "a", "to": "q1"},
            {"state": "q1", "symbol": "b", "to": "q1"},
            {"state": "q1", "symbol": "b", "to": "q2"},
            {"state": "q2", "symbol": "b", "to": "q3"},
            {"state": "q3", "symbol": "a", "to": "q1"},
            {"state": "q2", "symbol": "a", "to": "q4"},
        ]
        self.fa = FiniteAutomaton(self.states, self.alphabet, self.initial_state, self.final_state, self.transitions)

    def test_is_deterministic(self):
        # Test for deterministic automaton
        self.assertFalse(self.fa.is_deterministic())

        # Define a non-deterministic FA
        transitions_deterministic = [
            {"state": "q0", "symbol": "a", "to": "q1"},
            {"state": "q0", "symbol": "b", "to": "q2"}
        ]
        fa_deterministic = FiniteAutomaton(self.states, self.alphabet, self.initial_state, self.final_state,
                                           transitions_deterministic)
        self.assertTrue(fa_deterministic.is_deterministic())

    def test_convert_to_grammar(self):
        grammar = self.fa.convert_to_grammar()

        # Test the grammar's properties
        self.assertEqual(grammar.non_terminals, self.states)
        self.assertEqual(grammar.terminals, self.alphabet)
        self.assertEqual(grammar.start_symbols, self.initial_state)

        # Check some productions from the transitions
        productions = grammar.productions
        self.assertIn("q0", productions)
        self.assertIn("q1", productions)
        self.assertIn("q2", productions)

        # For example, check that the transition q0 -a-> q1 is translated to a production
        self.assertIn("aq1", productions["q0"])


if __name__ == '__main__':
    unittest.main()
