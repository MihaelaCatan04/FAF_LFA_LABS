from Lab1.src.FiniteAutomaton import FiniteAutomaton
from Lab1.src.Grammar import Grammar


def main():
    non_terminals = {"S", "I", "J", "K"}
    terminals = {"a", "b", "c", "e", "n", "f", "m"}
    productions = {
        'S': ['cI'],
        'I': ['bJ', 'fI', 'e', 'eK'],
        'J': ['nJ', 'cS'],
        'K': ['nK', 'm']
    }
    start_symbol = "S"

    grammar = Grammar(non_terminals, terminals, productions, start_symbol)
    # print(grammar.generate_strings(5))
    finite_automaton = FiniteAutomaton(grammar)
    print(finite_automaton.check_string("cbccfem"))

if __name__=="__main__":
    main()