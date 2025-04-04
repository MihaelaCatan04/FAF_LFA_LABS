# Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Mihaela Catan, st.gr.FAF-231
### Verified by: Dumitru Crețu, University Assistant 

----

## Theoretical Background

### Deterministic and Non-deterministic Finite Automata

A finite automaton (FA) is a mathematical model of computation with a finite number of states. It processes input symbols sequentially and transitions between states based on the current state and input symbol. Finite automata are classified into two main categories:

1. **Deterministic Finite Automaton (DFA)**: For each state and input symbol, there is exactly one transition to another state.
2. **Non-deterministic Finite Automaton (NFA)**: For a given state and input symbol, there can be multiple possible transitions to different states.

Despite their structural differences, DFAs and NFAs recognize the same class of languages—regular languages. Any NFA can be converted to an equivalent DFA through a systematic process.

### Regular Grammars and Finite Automata

There exists a direct correspondence between regular grammars (Type 3 in the Chomsky hierarchy) and finite automata:

1. Any language generated by a regular grammar can be recognized by a finite automaton.
2. Any language recognized by a finite automaton can be generated by a regular grammar.

This equivalence enables us to convert between the two representations while preserving the language they define.

### Chomsky Hierarchy

The Chomsky hierarchy, introduced by Noam Chomsky, categorizes formal grammars into four types:

1. **Type 0 (Unrestricted)**: No restrictions on production rules. These grammars generate recursively enumerable languages.
2. **Type 1 (Context-sensitive)**: Productions of the form αAβ → αγβ, where A is a non-terminal and γ is a non-empty string.
3. **Type 2 (Context-free)**: Productions of the form A → γ, where A is a non-terminal.
4. **Type 3 (Regular)**: Productions of the form A → a or A → aB, where A and B are non-terminals and a is a terminal.

Each type forms a proper subset of the previous type, with Type 3 being the most restrictive.

## Objectives

This laboratory work aims to:

1. Implement the conversion of a finite automaton to a regular grammar
2. Determine whether a given finite automaton is deterministic or non-deterministic
3. Implement conversion from NDFA to DFA
4. Represent the finite automaton graphically using external visualization tools
5. Provide a method to classify a grammar based on the Chomsky hierarchy

## Implementation Description

### FiniteAutomaton Class

The `FiniteAutomaton` class represents a finite automaton with the following components:
- States (Q)
- Alphabet (Σ)
- Initial state (q₀)
- Final states (F)
- Transitions (δ)

#### Method: `is_deterministic()`

This method determines whether the finite automaton is deterministic by checking if there are multiple transitions from the same state with the same input symbol:

```python
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
```

The method works by keeping track of state-symbol pairs that have been seen. If a pair appears more than once in the transitions, the automaton is non-deterministic.

Time complexity: O(n), where n is the number of transitions.

#### Method: `__get_productions()`

This private method generates production rules for a regular grammar based on the finite automaton's transitions:

```python
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
```

For each transition from state q to state p with input symbol a:
- If p is not a final state, add production q → ap
- If p is a final state, add production q → a

Time complexity: O(n), where n is the number of transitions.

#### Method: `convert_to_grammar()`

This method converts the finite automaton to a regular grammar:

```python
def convert_to_grammar(self):
    non_terminals = self.states
    terminals = self.alphabet
    initial_state = self.initial_state
    productions = self.__get_productions()
    grammar = Grammar(non_terminals, terminals, productions, initial_state)
    return grammar
```

The conversion follows these principles:
- States in the automaton become non-terminal symbols in the grammar
- Input symbols become terminal symbols
- Transitions are converted to production rules
- The initial state becomes the start symbol

Time complexity: O(n), where n is the number of transitions.

#### Method: `visualize()`

This method visualizes the finite automaton using Graphviz:

```python
def visualize(self):
    dot = Digraph(comment='Finite Automaton')

    for state in self.states:
        if state == self.initial_state:
            dot.node(state, shape='doublecircle', style='dashed')
        elif state in self.final_state:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for transition in self.transitions:
        dot.edge(transition["state"], transition["to"], label=transition["symbol"])

    dot.render('finite_automaton', format='png', view=True)
```

The visualization uses the following conventions:
- Initial state: dashed double circle
- Final states: double circle
- Regular states: simple circle
- Transitions: directed edges labeled with input symbols

#### Method: `convert_to_dfa()`

This method converts a non-deterministic finite automaton (NDFA) to a deterministic finite automaton (DFA):

```python
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
```
The method works by converting the NDFA states and transitions to equivalent DFA states and transitions.

Time complexity: O(n), where n is the number of transitions.

### Grammar Class

The `Grammar` class represents a formal grammar with the following components:
- Non-terminal symbols
- Terminal symbols
- Production rules
- Start symbol

```python
class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbols = start_symbol

    def print_grammar(self):
        print("Grammar:")
        print(f"Start Symbol: {self.start_symbols}")
        print("Non-Terminals:", ", ".join(self.non_terminals))
        print("Terminals:", ", ".join(self.terminals))
        print("Productions:")
        print(self.productions)
```

### Chomsky Hierarchy Classification

The `Grammar` class has been extended with methods to classify the grammar according to the Chomsky hierarchy:

```python
def __check_type3(self):
    type3 = True
    for non_terminal, production in self.productions.items():
        if non_terminal in self.non_terminals and len(non_terminal) == 1:
            for prod in production:
                # Check production rules for Type 3 grammar
                if len(prod) == 1 and prod in self.terminals:
                    continue
                elif len(prod) == 2 and prod[0] in self.terminals and prod[1] in self.non_terminals:
                    continue
                elif len(prod) == 2 and prod[0] in self.non_terminals and prod[1] in self.terminals:
                    continue
                else:
                    type3 = False
                    break
        else:
            type3 = False
            break
    return type3

def __check_type2(self):
    type2 = True
    for non_terminal, production in self.productions.items():
        if non_terminal in self.non_terminals and len(non_terminal) == 1:
            for prod in production:
                # Check if the production is valid for a Type 2 grammar
                if len(prod) == 0 or all(
                        symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                    continue
                else:
                    type2 = False
                    break
        else:
            type2 = False
            break
    return type2

def __check_type1(self):
    type1 = True
    for non_terminal, production in self.productions.items():
        if non_terminal in self.non_terminals:
            for prod in production:
                # Check if production is valid for Type 1 grammar
                if len(non_terminal) <= len(prod) and all(
                        symbol in self.terminals or symbol in self.non_terminals for symbol in prod):
                    continue
                else:
                    type1 = False
                    break
        else:
            type1 = False
            break
    return type1

def __check_type0(self):
    type0 = True
    for non_terminal, production in self.productions.items():
        if non_terminal in self.non_terminals:
            for prod in production:
                # Type 0 allows unrestricted production rules
                if all(symbol in self.terminals or symbol in self.non_terminals for symbol in prod) or len(
                        prod) == 0:
                    continue
                else:
                    type0 = False
                    break
        else:
            type0 = False
            break
    return type0

def return_grammar_type(self):
    # Check for Type 0, then Type 1, Type 2, and Type 3 in sequence
    if self.__check_type0():
        if self.__check_type1():
            if self.__check_type2():
                if self.__check_type3():
                    return "Grammar Type 3"
                else:
                    return "Grammar Type 2"
            else:
                return "Grammar Type 1"
        else:
            return "Grammar Type 0"
    else:
        return "Invalid Grammar Type"
```

#### Method Analysis: `__check_type3()`

This private method checks if the grammar is a Type 3 (Regular) grammar by verifying that all productions follow one of these patterns:
- A → a (a single terminal)
- A → aB (a terminal followed by a non-terminal)
- A → Ba (a non-terminal followed by a terminal, for left-regular grammars)

The method ensures that non-terminals are single characters and that all productions follow these rigid constraints.

Time complexity: O(n × m), where n is the number of non-terminals and m is the average number of productions per non-terminal.

#### Method Analysis: `__check_type2()`

This private method checks if the grammar is a Type 2 (Context-Free) grammar by verifying that:
- All non-terminals are single characters
- Each production has a single non-terminal on the left-hand side
- The right-hand side can be any combination of terminals and non-terminals

Time complexity: O(n × m × k), where n is the number of non-terminals, m is the average number of productions per non-terminal, and k is the average length of production right-hand sides.

#### Method Analysis: `__check_type1()`

This private method checks if the grammar is a Type 1 (Context-Sensitive) grammar by verifying that:
- The length of the right-hand side of each production is not shorter than the left-hand side
- All symbols used are either terminals or non-terminals

This ensures that context-sensitive properties are maintained, where the context around a non-terminal determines how it can be replaced.

Time complexity: O(n × m × k), where n is the number of non-terminals, m is the average number of productions per non-terminal, and k is the average length of production right-hand sides.

#### Method Analysis: `__check_type0()`

This private method checks if the grammar is a Type 0 (Unrestricted) grammar by verifying that:
- All symbols used are either terminals or non-terminals
- Empty productions are allowed

Type 0 grammars have the least restrictions, allowing for the most expressive power.

Time complexity: O(n × m × k), where n is the number of non-terminals, m is the average number of productions per non-terminal, and k is the average length of production right-hand sides.

#### Method Analysis: `return_grammar_type()`

This method determines the type of grammar based on the Chomsky hierarchy by checking each type in sequence, from the most restrictive (Type 3) to the least restrictive (Type 0). It returns a string indicating the grammar type.

The method leverages the hierarchical nature of the Chomsky hierarchy, where each type is a subset of the previous type. By checking in this specific order, the method correctly identifies the most restrictive classification that applies to the grammar.

Time complexity: O(n × m × k), where n is the number of non-terminals, m is the average number of productions per non-terminal, and k is the average length of production right-hand sides.

## Testing and Results

### Testing the Finite Automaton

The test class `TestFiniteAutomaton` verifies the functionality of the `FiniteAutomaton` class:

```python
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
        self.assertFalse(self.fa.is_deterministic())

        transitions_deterministic = [
            {"state": "q0", "symbol": "a", "to": "q1"},
            {"state": "q0", "symbol": "b", "to": "q2"}
        ]
        fa_deterministic = FiniteAutomaton(self.states, self.alphabet, self.initial_state, self.final_state,
                                        transitions_deterministic)
        self.assertTrue(fa_deterministic.is_deterministic())

    def test_convert_to_grammar(self):
        grammar = self.fa.convert_to_grammar()

        self.assertEqual(grammar.non_terminals, self.states)
        self.assertEqual(grammar.terminals, self.alphabet)
        self.assertEqual(grammar.start_symbols, self.initial_state)

        productions = grammar.productions
        self.assertIn("q0", productions)
        self.assertIn("q1", productions)
        self.assertIn("q2", productions)

        self.assertIn("aq1", productions["q0"])
```

### Results

This laboratory work successfully addressed the objectives related to finite automata and formal languages within the Chomsky hierarchy. The implementation demonstrated:

1. A comprehensive conversion of finite automata to regular grammars through the `convert_to_grammar()` method, accurately transforming states to non-terminals and transitions to production rules.

2. A reliable determinism checker through the `is_deterministic()` method, which correctly identified when multiple transitions exist for the same state-input pair.

3. The visualization capability provided through Graphviz integration offered a clear graphical representation of finite automata with appropriate notations for initial, final, and regular states.

4. The classification of grammars according to the Chomsky hierarchy was successfully implemented through a hierarchical approach that checks grammar types in sequence from Type 3 (most restrictive) to Type 0 (unrestricted).

The test results confirmed the accuracy of the implementation, showing that the determinism check correctly identified deterministic and non-deterministic automata, and that the grammar conversion properly maintained the structural relationships between the automaton's components.

Through this work, the fundamental theoretical concepts of formal languages—particularly the relationship between finite automata and regular grammars—were effectively demonstrated in practice, providing a solid foundation for understanding more complex language processing systems.
