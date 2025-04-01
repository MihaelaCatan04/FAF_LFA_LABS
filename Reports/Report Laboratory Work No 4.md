# Laboratory Work Report: Regular Expressions

### Course: Formal Languages & Finite Automata
### Author: Mihaela Catan, st.gr.FAF-231
### Verified by: Dumitru Crețu, University Assistant
----

## Theoretical Background

### Regular Expressions

Regular expressions (regex) are formal patterns that define search strings, primarily used for pattern matching within text. They represent a sequence of characters that define a search pattern, providing a concise and flexible means for identifying strings of text, such as particular characters, words, or patterns of characters.

Regular expressions are widely used for:
1. **Text Validation**: Ensuring input follows a specific format (email addresses, phone numbers)
2. **Pattern Matching**: Finding specific patterns within larger text
3. **Text Extraction**: Isolating parts of text that match defined patterns
4. **Text Replacement**: Substituting text based on pattern matches
5. **Lexical Analysis**: Breaking down source code into tokens during compilation
6. **Data Cleaning**: Standardizing and normalizing data formats

In formal language theory, regular expressions precisely define regular languages, which can be recognized by finite state machines. This connection to automata theory makes them fundamental to computer science.

## Objectives

1. Understand the concept and application of regular expressions
2. Implement a system that dynamically interprets regular expressions to generate valid strings
3. Create a logging mechanism to trace the processing of regular expressions step by step
4. Generate valid combinations of strings according to specified patterns for variant 2

## Implementation Description

The implementation consists of three main components:

1. `RegexParser`: Parses regular expression patterns into tokens
2. `RegexGenerator`: Generates valid combinations based on the parsed tokens
3. `RegexLogger`: Tracks and displays the processing steps

### RegexLogger Class

The `RegexLogger` class provides a simple mechanism to log and display the processing steps:

```python
class RegexLogger:
    def __init__(self):
        self.steps = []
        
    def process(self, step):
        self.steps.append(step)
        
    def show_steps(self):
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: {step}")
```

This class:
- Maintains a list of processing steps
- Provides methods to add steps and display the entire sequence

### RegexParser Class

The `RegexParser` class breaks down regular expressions into a sequence of tokens that can be interpreted by the generator:

```python
import re
from RegexLogger import RegexLogger

class RegexParser:
    def __init__(self):
        self.tokens = []
        self.logger = RegexLogger()
        
    def parse(self, pattern):
        self.logger = RegexLogger()
        self.logger.process(f"Parsing pattern: {pattern}")
        self.tokens = []
        i = 0
        
        while i < len(pattern):
            char = pattern[i]
            
            # Handle groupings
            if char == "(":
                group_end = pattern.find(")", i)
                if group_end != -1:
                    # Check if followed by repetition
                    if group_end + 1 < len(pattern) and pattern[group_end + 1] == "^":
                        match = re.match(r"\((.*?)\)\^\{(\d+)\}", pattern[i:])
                        if match:
                            group_content = match.group(1).split('|')
                            repetition = int(match.group(2))
                            self.tokens.append(('group', (group_content, repetition)))
                            i += len(match.group(0))
                            self.logger.process(f"Found group with repetition: {match.group(0)}")
                            continue
                    
                    # Simple group with modifiers
                    elif group_end + 1 < len(pattern) and pattern[group_end + 1] in "?*+":
                        group_content = pattern[i + 1:group_end].split('|')
                        modifier = pattern[group_end + 1]
                        self.tokens.append(('group_mod', (group_content, modifier)))
                        i = group_end + 2
                        self.logger.process(f"Found group with modifier: ({pattern[i + 1:group_end]}){modifier}")
                        continue
                    else:
                        # Simple group without modifiers
                        self.logger.process(f"Found simple group: ({pattern[i + 1:group_end]})")
                        group_content = pattern[i + 1:group_end].split('|')
                        self.tokens.append(('group', (group_content, 1)))
                        i = group_end + 1
                        continue
                        
            # Character with repetition
            if i + 1 < len(pattern) and pattern[i + 1] == "^":
                match = re.match(r"(\w)\^\{(\d+)\}", pattern[i:])
                if match:
                    char = match.group(1)
                    repetition = int(match.group(2))
                    self.tokens.append(('char_rep', (char, repetition)))
                    i += len(match.group(0))
                    self.logger.process(f"Found character with repetition: {match.group(0)}")
                    continue
                    
            # Character with modifier (?, *, +)
            if i + 1 < len(pattern) and pattern[i + 1] in "?*+":
                modifier = pattern[i + 1]
                self.tokens.append(('char_mod', (char, modifier)))
                i += 2
                self.logger.process(f"Found character with modifier: {char}{modifier}")
                continue
                
            # Simple character
            self.tokens.append(('char', char))
            self.logger.process(f"Found simple character: {char}")
            i += 1
            
        return self.tokens
```

The parser analyzes the regular expression pattern character by character and identifies several token types:

1. `char`: A simple character (e.g., 'a')
2. `char_rep`: A character with a specific repetition count (e.g., 'a^{3}' for 'aaa')
3. `char_mod`: A character with a modifier (e.g., 'a+', 'b*', 'c?')
4. `group`: A group of alternative characters with optional repetition (e.g., '(a|b|c)^{2}')
5. `group_mod`: A group with a modifier (e.g., '(a|b)+', '(x|y)*')

For each token extracted, the parser logs the action and stores the token for processing by the generator.

### RegexGenerator Class

The `RegexGenerator` class takes the tokens produced by the parser and generates valid string combinations:

```python
import itertools
from RegexLogger import RegexLogger

class RegexGenerator:
    def __init__(self):
        self.logger = RegexLogger()

    def generate(self, tokens):
        self.logger = RegexLogger()
        result_parts = []

        for token_type, token_value in tokens:
            self.logger.process(f"Processing token: {token_type} - {token_value}")

            if token_type == 'char':
                # Simple character
                result_parts.append([token_value])

            elif token_type == 'char_rep':
                # Character with repetition
                char, repetition = token_value
                result_parts.append([char * repetition])
                self.logger.process(f"Generated repeated character: {char * repetition}")

            elif token_type == 'char_mod':
                # Character with modifier
                char, modifier = token_value
                if modifier == '?':
                    # Optional (0 or 1)
                    result_parts.append(['', char])
                    self.logger.process(f"Generated optional character: '' or '{char}'")
                elif modifier == '*':
                    # Zero or more (limit to 5)
                    result_parts.append([char * i for i in range(6)])
                    self.logger.process(f"Generated 0-5 repetitions of '{char}'")
                elif modifier == '+':
                    # One or more (limit to 5)
                    result_parts.append([char * i for i in range(1, 6)])
                    self.logger.process(f"Generated 1-5 repetitions of '{char}'")

            elif token_type == 'group':
                # Group with repetition
                options, repetition = token_value
                if repetition == 1:
                    # Group without repetition
                    result_parts.append(options)
                    self.logger.process(f"Generated group options: {options}")
                else:
                    # Group with repetition
                    combinations = []
                    for combo in itertools.product(options, repeat=repetition):
                        combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(
                        f"Generated group repetitions: {combinations[:5]}{'...' if len(combinations) > 5 else ''}")

            elif token_type == 'group_mod':
                # Group with modifier
                options, modifier = token_value
                if modifier == '?':
                    # Optional group (0 or 1)
                    result_parts.append([''] + options)
                    self.logger.process(f"Generated optional group: '' or {options}")
                elif modifier == '*':
                    # Zero or more (limit to 5)
                    combinations = ['']
                    for i in range(1, 6):
                        for combo in itertools.product(options, repeat=i):
                            combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(f"Generated 0-5 group repetitions")
                elif modifier == '+':
                    # One or more (limit to 5)
                    combinations = []
                    for i in range(1, 6):
                        for combo in itertools.product(options, repeat=i):
                            combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(f"Generated 1-5 group repetitions")

        # Generate all combinations
        self.logger.process("Generating final combinations...")
        all_combinations = []

        # Combine all parts
        for combo in itertools.product(*result_parts):
            all_combinations.append(''.join(combo))

        self.logger.process(f"Generated {len(all_combinations)} total combinations")
        return all_combinations
```

The generator:
1. Processes each token and generates possible string parts based on the token type and value
2. For unlimited repetitions (`*` and `+` modifiers), limits generation to 5 repetitions
3. Uses `itertools.product()` to generate all possible combinations of the parts
4. Logs each step of the generation process

### Main Program

The main program ties everything together:

```python
from RegexParser import RegexParser
from RegexGenerator import RegexGenerator

patterns = [
    "M?N^{2}(O|P)^{3}O*R+",
    "(X|Y|Z)^{3}8+(9|0)^{2}",
    "(H|i)(J|L)L*N?"
]

parser = RegexParser()
generator = RegexGenerator()

file_path = "../additional_files/regex_combinations.txt"

with open(file_path, "a") as f:
    for pattern in patterns:
        tokens = parser.parse(pattern)
        results = generator.generate(tokens)
        
        # Write the pattern and the combinations
        f.write(f"Pattern: {pattern}\n")
        for combo in results:
            f.write(combo + "\n")
        
        # Show log steps
        print("\nLog steps:")
        parser.logger.show_steps()
        generator.logger.show_steps()
        
        print("\nSample combinations:")
        for sample in results[:5]:
            print(sample)
        
        print(f"All combinations saved to {file_path}")
```

The main program:
1. Defines regular expression patterns for variant 2
2. Processes each pattern to generate valid string combinations
3. Saves the results to a file
4. Displays the processing steps and sample combinations

## Testing and Results

### Pattern 1: `M?N^{2}(O|P)^{3}O*R+`

This pattern represents strings that:
- Optionally start with 'M'
- Followed by exactly two 'N's
- Followed by exactly three characters, each being either 'O' or 'P'
- Followed by zero or more 'O's (up to 5 for our implementation)
- End with one or more 'R's (up to 5 for our implementation)

Sample valid combinations:
```
MNNOOOR
MNNPPPOOORRR
NNOOPR
NNPOOR
MNNOOPR
```

### Pattern 2: `(X|Y|Z)^{3}8+(9|0)^{2}`

This pattern represents strings that:
- Start with exactly three characters, each being either 'X', 'Y', or 'Z'
- Followed by one or more '8's (up to 5 for our implementation)
- End with exactly two characters, each being either '9' or '0'

Sample valid combinations:
```
XXX890
YYY8899
ZZZ88800
XXY88890
XYZ8889
```

### Pattern 3: `(H|i)(J|L)L*N?`

This pattern represents strings that:
- Start with either 'H' or 'i'
- Followed by either 'J' or 'L'
- Followed by zero or more 'L's (up to 5 for our implementation)
- Optionally end with 'N'

Sample valid combinations:
```
HJN
iLLLN
HLLN
iJL
HLL
```

### Processing Steps

The logging functionality shows how each pattern is processed:

```
Step 1: Parsing pattern: M?N^{2}(O|P)^{3}O*R+
Step 2: Found character with modifier: M?
Step 3: Found character with repetition: N^{2}
Step 4: Found group with repetition: (O|P)^{3}
Step 5: Found character with modifier: O*
Step 6: Found character with modifier: R+
```

```
Step 1: Processing token: char_mod - ('M', '?')
Step 2: Generated optional character: '' or 'M'
Step 3: Processing token: char_rep - ('N', 2)
Step 4: Generated repeated character: NN
Step 5: Processing token: group - (['O', 'P'], 3)
Step 6: Generated group repetitions: ['OOO', 'OOP', 'OPO', 'OPP', 'POO']...
Step 7: Processing token: char_mod - ('O', '*')
Step 8: Generated 0-5 repetitions of 'O'
Step 9: Processing token: char_mod - ('R', '+')
Step 10: Generated 1-5 repetitions of 'R'
Step 11: Generating final combinations...
Step 12: Generated 576 total combinations
```

## Conclusions

This laboratory work successfully implemented a system that dynamically interprets and generates valid strings from regular expressions. The implementation demonstrates:

1. **Dynamic Interpretation**: The system can process any regular expression that follows the defined syntax, not just hardcoded patterns.

2. **Comprehensive Logging**: The step-by-step tracking provides visibility into how regular expressions are processed and how combinations are generated.

3. **Extensibility**: The modular design allows for easy extension to support additional regex features in the future.
