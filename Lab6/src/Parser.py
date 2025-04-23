from Lab6.src.IngredientNode import IngredientNode
from Lab6.src.NumberNode import NumberNode
from Lab6.src.RecipeNode import RecipeNode
from Lab6.src.StepNode import StepNode
from Lab6.src.StringNode import StringNode
from Lab6.src.TemperatureNode import TemperatureNode
from Lab6.src.TimeNode import TimeNode
from Lab6.src.TitleNode import TitleNode
from Lab6.src.TokenType import TokenType
from Lab6.src.UnitNode import UnitNode
from Lab6.src.YieldNode import YieldNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.parse_recipe()

    def parse_recipe(self):
        # Expect RECIPE token
        self.consume(TokenType.RECIPE)
        self.consume(TokenType.LBRACE)

        # Initialize an empty Recipe node
        recipe = RecipeNode()

        # Parse recipe components until we hit the closing brace
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.TITLE):
                self.consume(TokenType.TITLE)
                self.consume(TokenType.COLON)
                title_value = self.consume(TokenType.STRING).value.strip('"')
                self.consume(TokenType.SEMICOLON)
                recipe.title = TitleNode(StringNode(title_value))

            elif self.check(TokenType.YIELD):
                self.consume(TokenType.YIELD)
                self.consume(TokenType.COLON)
                yield_value = float(self.consume(TokenType.NUMBER).value)
                self.consume(TokenType.SEMICOLON)
                recipe.yield_node = YieldNode(NumberNode(yield_value))

            elif self.check(TokenType.TIME):
                self.consume(TokenType.TIME)
                self.consume(TokenType.COLON)
                time_value = float(self.consume(TokenType.NUMBER).value)
                time_unit = self.consume(TokenType.TIME_UNIT).value
                self.consume(TokenType.SEMICOLON)
                recipe.time_node = TimeNode(NumberNode(time_value), UnitNode(time_unit))

            elif self.check(TokenType.INGREDIENT):
                self.consume(TokenType.INGREDIENT)
                self.consume(TokenType.COLON)

                quantity = NumberNode(float(self.consume(TokenType.NUMBER).value))

                unit = None
                if self.check(TokenType.UNIT):
                    unit = UnitNode(self.consume(TokenType.UNIT).value)

                name = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)

                recipe.ingredients.append(IngredientNode(quantity, unit, name))

            elif self.check(TokenType.STEP):
                self.consume(TokenType.STEP)
                self.consume(TokenType.COLON)
                instruction = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)

                recipe.steps.append(StepNode(instruction))

            elif self.check(TokenType.TEMP):
                self.consume(TokenType.TEMP)
                self.consume(TokenType.COLON)
                temp_value = NumberNode(float(self.consume(TokenType.NUMBER).value))
                temp_unit = UnitNode(self.consume(TokenType.TEMP_UNIT).value)
                self.consume(TokenType.SEMICOLON)

                recipe.temperature = TemperatureNode(temp_value, temp_unit)

            else:
                # Skip unknown tokens
                self.advance()

        self.consume(TokenType.RBRACE)

        return recipe

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, token_type):
        if self.check(token_type):
            return self.advance()

        raise SyntaxError(f"Expected {token_type} but got {self.peek().token_type}")

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]