import unittest

from Lab1.src.Grammar import Grammar


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.non_terminals = {"S", "I", "J", "K"}
        self.terminals = {"a", "b", "c", "e", "n", "f", "m"}
        self.productions = {
            'S': ['cI'],
            'I': ['bJ', 'fI', 'e', 'eK'],
            'J': ['nJ', 'cS'],
            'K': ['nK', 'm']
        }
        self.start_symbol = "S"
        self.grammar = Grammar(self.non_terminals, self.terminals, self.productions, self.start_symbol)

    def test_generate_string_contains_only_terminals(self):
        generated_string = self.grammar.generate_string()
        for char in generated_string:
            self.assertIn(char, self.terminals, f"Non-terminal '{char}' found in generated string.")

    def test_generate_multiple_strings(self):
        num_strings = 5
        generated_strings = self.grammar.generate_strings(num_strings)
        self.assertEqual(len(generated_strings), num_strings, "Incorrect number of strings generated.")

    def test_generated_strings_are_not_empty(self):
        generated_string = self.grammar.generate_string()
        self.assertTrue(len(generated_string) > 0, "Generated string is empty.")

    def test_productions_are_followed(self):
        generated_string = self.grammar.generate_string()
        self.assertTrue(all(char in self.terminals for char in generated_string), "Invalid production used.")

    def test_empty_productions(self):
        empty_production_grammar = Grammar({"S"}, {"a", "b"}, {'S': ['']}, "S")
        generated_string = empty_production_grammar.generate_string()
        self.assertEqual(generated_string, "", "Generated string should be empty.")


if __name__ == "__main__":
    unittest.main()