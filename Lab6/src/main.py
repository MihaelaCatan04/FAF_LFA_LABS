from Lab6.src.Lexer import Lexer
from Lab6.src.Parser import Parser

test_recipe = '''
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
'''

lexer = Lexer()
tokens = lexer.tokenize(test_recipe)

print("Tokens:")
for token in tokens:
    print(token)
print()

parser = Parser(tokens)
recipe_ast = parser.parse()


