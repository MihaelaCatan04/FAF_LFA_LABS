import unittest

from Lab1.src.FiniteAutomaton import FiniteAutomaton
from Lab1.src.Grammar import Grammar


class TestFiniteAutomaton(unittest.TestCase):
    # Set up the test environment
    def setUp(self):
        non_terminals = {"S", "I", "J", "K"}
        terminals = {"a", "b", "c", "e", "n", "f", "m"}
        productions = {
            'S': ['cI'],
            'I': ['bJ', 'fI', 'e', 'eK'],
            'J': ['nJ', 'cS'],
            'K': ['nK', 'm']
        }
        start_symbol = "S"
        self.grammar = Grammar(non_terminals, terminals, productions, start_symbol)
        self.finite_automaton = FiniteAutomaton(self.grammar)

    # Test case: Check if the string "cbccfem" is accepted by the finite automaton
    def test_check_valid_string(self):
        result = self.finite_automaton.check_string("cbccfem")
        self.assertTrue(result)

    # Test case: Check if the string "cbccf" is rejected by the finite automaton
    def test_check_invalid_string(self):
        result = self.finite_automaton.check_string("cbccf")
        self.assertFalse(result)

    # Test case: Check if an empty string is rejected by the finite automaton
    def test_empty_string(self):
        result = self.finite_automaton.check_string("")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
