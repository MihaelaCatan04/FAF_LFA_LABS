# Laboratory Work Report:Parser & Building an AST

### Course: Formal Languages & Finite Automata
### Author: Mihaela Catan, st.gr.FAF-231
### Verified by: Dumitru Crețu, University Assistant

## Theory
Domain-Specific Languages (DSLs) are specialized languages designed for particular application domains. They offer a way to express domain concepts in a concise, readable, and maintainable manner. A Recipe DSL, as implemented in this laboratory work, provides a formalized way to represent cooking recipes, including ingredients, steps, timing, and temperature information.
The process of implementing a DSL involves several key components:

1. Lexical Analysis: Converting source code into tokens
2. Parsing: Creating an Abstract Syntax Tree (AST) from tokens
3. Abstract Syntax Tree: In-memory representation of the program structure
4. Visualization: Displaying the AST to understand the structure

## Objectives:

1. Understand the concept of Domain-Specific Languages and their applications
2. Learn the process of implementing a lexer and parser for a DSL
3. Implement an Abstract Syntax Tree representation for a Recipe language
4. Visualize the AST for better understanding of program structure

## Implementation Description
### Lexical Analysis
The lexical analyzer (lexer) breaks down the input text into a sequence of tokens, identifying keywords, literals, and symbols according to defined patterns. For our Recipe DSL, we define token types using the Enum class and implement pattern matching with regular expressions.
```python
class TokenType(Enum):
    # Keywords
    RECIPE = auto()
    TITLE = auto()
    INGREDIENT = auto()
    STEP = auto()
    YIELD = auto()
    TIME = auto()
    TEMP = auto()
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    
    # Units
    UNIT = auto()
    TIME_UNIT = auto()
    TEMP_UNIT = auto()
    
    # Identifiers
    ID = auto()
    
    # Symbols
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Special
    EOF = auto()
```
The Lexer class implements the tokenization process using regular expressions to match patterns in the input text:
```python
def tokenize(self, text):
    self.tokens = []
    position = 0
    
    while position < len(text):
        match_found = False

        for token_type, pattern in self.token_patterns:
            regex = re.compile(f'^{pattern}', re.IGNORECASE)
            match = regex.match(text[position:])

            if match:
                value = match.group(0)

                if token_type is not None:  # Skip whitespace
                    self.tokens.append(Token(token_type, value))

                position += len(value)
                match_found = True
                break

        if not match_found:
            raise ValueError(f"Unrecognized token at position {position}")

    self.tokens.append(Token(TokenType.EOF, ''))
    return self.tokens
```
This method scans the input text character by character, attempting to match token patterns. When a match is found, it creates a token with the appropriate type and value, then advances the position. This process continues until the entire input is processed.
### Abstract Syntax Tree (AST)

The AST represents the hierarchical structure of the recipe. We define several node types to represent different elements of a recipe:
```python
class RecipeNode(ASTNode):
    def __init__(self):
        self.title = None
        self.yield_node = None
        self.time_node = None
        self.ingredients = []
        self.steps = []
        self.temperature = None
```
Other node types include IngredientNode, StepNode, TimeNode, TemperatureNode, etc., each capturing specific aspects of the recipe structure.
### Parsing
The parser converts the sequence of tokens into an AST. It implements recursive descent parsing, where each grammar rule is represented by a parsing method:
```python
def parse_recipe(self):
    self.consume(TokenType.RECIPE)
    self.consume(TokenType.LBRACE)
    
    recipe = RecipeNode()
    
    while not self.check(TokenType.RBRACE) and not self.is_at_end():
        if self.check(TokenType.TITLE):
            self.consume(TokenType.TITLE)
            self.consume(TokenType.COLON)
            title_value = self.consume(TokenType.STRING).value.strip('"')
            self.consume(TokenType.SEMICOLON)
            recipe.title = TitleNode(StringNode(title_value))
        
    self.consume(TokenType.RBRACE)
    
    return recipe
```
The parser walks through the tokens, consuming them as it builds up the AST. It uses methods like consume() to match expected tokens and check() to look ahead without consuming tokens.
### AST Visualization
To better understand the structure of the parsed recipe, we implement visualization using graphviz:
```python
class ASTVisualizer:
    
    def __init__(self):
        self.dot = graphviz.Digraph(comment='Recipe AST')
        self.node_count = 0
    
    def visualize(self, node):
        self._add_node(node)
        return self.dot
```
The visualizer recursively traverses the AST, creating nodes and edges in the graphviz diagram to represent the hierarchical structure of the recipe.
## Results
To test the implementation, we used a sample recipe for Basic Tomato Sauce:
```RECIPE {
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
After running our parser on this input, we obtained the following tokens:
```Token(TokenType.RECIPE, 'RECIPE')
Token(TokenType.LBRACE, '{')
Token(TokenType.TITLE, 'TITLE')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Basic Tomato Sauce"')
Token(TokenType.SEMICOLON, ';')
...
```
And the following Abstract Syntax Tree:
```RECIPE
  TITLE
    STRING: "Basic Tomato Sauce"
  YIELD
    NUMBER: 6.0
  TIME
    duration
      NUMBER: 45.0
    unit
      UNIT: min
  INGREDIENTS_LIST
    INGREDIENT
      quantity
        NUMBER: 800.0
      unit
        UNIT: g
      name
        STRING: "canned tomatoes"
    ...
  STEPS_LIST
    STEP
      instruction
        STRING: "Heat oil in a large saucepan"
    ...
  TEMPERATURE
    value
      NUMBER: 120.0
    unit
      UNIT: C
```
The visualization of this AST shows a clear hierarchical structure representing the recipe, with properly connected nodes for title, yield, time, ingredients, steps, and temperature.
## Conclusion
This laboratory work provided an in-depth exploration of Domain-Specific Language implementation through the creation of a Recipe DSL parser. The systematic approach, from lexical analysis to AST construction and visualization, demonstrated the key components involved in language processing.
The recipe language parser successfully transforms a structured recipe description into a formal representation that could be further processed for various applications, such as automated cooking instructions, recipe scaling, or nutritional analysis.
The implementation highlights the importance of proper tokenization, parsing strategies, and abstract syntax tree design. Each component plays a crucial role in accurately capturing the semantics of the domain, in this case, cooking recipes.
This exercise not only reinforced theoretical concepts in language processing but also enhanced practical skills in implementing lexers, parsers, and tree-based data structures. The visualization component further aids in understanding the structure of parsed recipes, making the implementation more accessible and intuitive.
Future enhancements could include semantic analysis, error recovery mechanisms, and code generation for specific applications in the culinary domain.
