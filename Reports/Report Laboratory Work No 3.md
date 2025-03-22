# Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Mihaela Catan, st.gr.FAF-231
### Verified by: Dumitru Crețu, University Assistant

----

## Theoretical Background

### Lexical Analysis and Tokenization

Lexical analysis, also known as scanning or tokenization, is the first phase of a compiler or interpreter that processes input text. The lexer (or scanner) reads the source code character by character and converts it into a sequence of tokens. These tokens serve as the basic building blocks for the next stages of compilation or interpretation.

Key concepts in lexical analysis include:

1. **Tokens**: Categorized units of text in the source code (e.g., identifiers, keywords, operators, literals).
2. **Lexemes**: The actual character sequences that match a specific token pattern.
3. **Patterns**: Rules that define what constitutes a valid token, often expressed as regular expressions.

The main difference between lexemes and tokens is that lexemes represent the actual text sequences, while tokens categorize these sequences based on language rules. For example, in a programming language, the lexeme "while" would be categorized as a KEYWORD token.

### Role of a Lexer

A lexer serves several important purposes in language processing:

1. **Simplification**: It abstracts away the character-by-character details of source code, providing higher-level tokens to the parser.
2. **Error Detection**: It identifies invalid character sequences that don't match any token patterns.
3. **Whitespace Handling**: It typically removes or ignores whitespace and comments that aren't semantically significant.
4. **Line and Column Tracking**: Many lexers keep track of source code positions for error reporting.

### Regular Expressions in Lexical Analysis

Regular expressions are particularly well-suited for lexical analysis because they can efficiently describe the patterns that define tokens. Each token type is associated with a regular expression pattern, and the lexer matches these patterns against the input text to identify tokens.

## Objectives

This laboratory work aims to:

1. Understand the concept and purpose of lexical analysis in language processing
2. Implement a functional lexer for a domain-specific language
3. Apply regular expressions to define token patterns
4. Demonstrate the lexer's operation on sample input

## Implementation Description

### Recipe Language Specification

The implemented lexer processes a domain-specific language for recipe descriptions. This language follows a structured format with specific keywords and syntax rules:

- **RECIPE**: Defines the beginning of a recipe block
- **TITLE**: Specifies the recipe name
- **INGREDIENT**: Lists required ingredients with quantities and units
- **STEP**: Describes preparation steps
- **YIELD**: Indicates the number of servings
- **TIME**: Specifies preparation/cooking time
- **TEMP**: Indicates cooking temperature

### Lexer Class

The `Lexer` class is responsible for breaking down recipe text into tokens using regular expressions:

```python
class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_patterns = {
            'KEYWORD': r'(RECIPE|TITLE|INGREDIENT|STEP|YIELD|TIME|TEMP)',
            'STRING': r'"[^"]*"',
            'NUMBER': r'[0-9]+(\.[0-9]+)?',
            'UNIT': r'(g|ml|tsp|tbsp|cup)',
            'TIME_UNIT': r'(min|hr)',
            'TEMP_UNIT': r'(C|F)',
            'ID': r'[a-zA-Z][a-zA-Z0-9_]*',
            'COLON': r':',
            'SEMICOLON': r';',
            'COMMA': r',',
            'LBRACE': r'{',
            'RBRACE': r'}',
            'WHITESPACE': r'[ \t\n]+'
        }
```

The class contains:
- A list to store generated tokens
- A dictionary mapping token types to their corresponding regular expression patterns

#### Method: `tokenize(text)`

This method processes the input text character by character, matching token patterns and generating tokens:

```python
def tokenize(self, text):
    self.tokens = []
    position = 0
    while position < len(text):
        match_found = False

        for token_type, pattern in self.token_patterns.items():
            regex = re.compile(f'^{pattern}', re.IGNORECASE)
            match = regex.match(text[position:])

            if match:
                value = match.group(0)

                if token_type != 'WHITESPACE':
                    self.tokens.append(Token(token_type, value))

                position += len(value)
                match_found = True
                break

        if not match_found:
            raise ValueError(f"Unrecognized token at position {position}: '{text[position:position + 10]}'")

    self.tokens.append(Token('EOF', ''))
    return self.tokens
```

The method works as follows:
1. It iterates through the input text, maintaining the current position
2. For each position, it tries to match one of the token patterns
3. When a match is found, a token is created (except for whitespace)
4. The position is advanced by the length of the matched text
5. If no pattern matches the current text position, an error is raised
6. Finally, an EOF token is added to signal the end of input

Time complexity: O(n × m), where n is the length of the input text and m is the number of token patterns.

### Token Structure

The token structure is implemented using a named tuple for simplicity and clarity:

```python
Token = namedtuple('Token', ['token_type', 'value'])
```

Each token has two attributes:
- `token_type`: The category of the token (e.g., KEYWORD, STRING, NUMBER)
- `value`: The actual text (lexeme) that was matched

### Regular Expression Patterns

The lexer uses several specialized regular expression patterns:

1. **KEYWORD**: Matches predefined language keywords (e.g., RECIPE, TITLE)
2. **STRING**: Matches text enclosed in double quotes
3. **NUMBER**: Matches integers and decimal numbers
4. **UNIT**: Matches cooking measurement units (e.g., g, ml, tsp)
5. **TIME_UNIT**: Matches time units (min, hr)
6. **TEMP_UNIT**: Matches temperature units (C, F)
7. **ID**: Matches identifiers starting with a letter
8. **COLON**, **SEMICOLON**, **COMMA**, **LBRACE**, **RBRACE**: Match specific punctuation characters
9. **WHITESPACE**: Matches spaces, tabs, and newlines (ignored in the token stream)

## Testing and Results

### Test Input

The lexer was tested using a sample recipe for tomato sauce:

```
RECIPE {
  TITLE: "Basic Tomato Sauce";

  YIELD: 6;
  TIME: 45 min;

  INGREDIENT: 800 g "canned tomatoes";
  INGREDIENT: 2 tbsp "olive oil";
  INGREDIENT: 1 "onion";
  INGREDIENT: 2 "garlic cloves";
  INGREDIENT: 1 tsp "salt";
  INGREDIENT: 0.5 tsp "black pepper";
  INGREDIENT: 1 tsp "dried basil";

  STEP: "Heat oil in a large saucepan";
  STEP: "Dice onion and garlic finely";
  STEP: "Sauté onion until translucent";
  STEP: "Add garlic and cook for 1 minute";
  STEP: "Add tomatoes and seasonings";
  STEP: "Simmer on low heat for 30 minutes";
  STEP: "Blend if smooth texture is desired";

  TEMP: 120 C;
}
```

### Test Results

The lexer successfully processed the input and produced the following token sequence (truncated for brevity):

```
[Token(token_type='KEYWORD', value='RECIPE'), 
 Token(token_type='LBRACE', value='{'), 
 Token(token_type='KEYWORD', value='TITLE'), 
 Token(token_type='COLON', value=':'), 
 Token(token_type='STRING', value='"Basic Tomato Sauce"'), 
 Token(token_type='SEMICOLON', value=';'),
 ... 
 Token(token_type='EOF', value='')]
```

Each token correctly identifies both the type and the actual value from the input text. The lexer properly handled:
- Keywords for recipe structure
- String literals for ingredient names and steps
- Numeric values for quantities
- Units for measurements
- Punctuation for syntax

## Conclusions

This laboratory work successfully implemented a lexer for a domain-specific language focused on recipe descriptions. The lexer demonstrates the fundamental concepts of lexical analysis:

1. It breaks down input text into meaningful tokens using regular expressions
2. It correctly categorizes different parts of the recipe syntax
3. It handles various data types including strings, numbers, and identifiers
4. It provides error detection for invalid input

The implementation shows how regular expressions can be effectively used to define token patterns in a lexical analyzer. The modular design with separate token type definitions allows for easy extension or modification of the language grammar.

Through this work, we gained practical understanding of lexical analysis and its role as the first stage in language processing. The recipe language parser serves as a concrete example of how domain-specific languages can be processed systematically.

By successfully implementing and testing the lexer with sample recipes, the objectives of this laboratory work were accomplished, demonstrating both the theoretical understanding and practical application of lexical analysis concepts.
