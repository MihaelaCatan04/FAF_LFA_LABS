from Lab6.src.AST import ASTNode


class RecipeNode(ASTNode):

    def __init__(self):
        self.title = None
        self.yield_node = None
        self.time_node = None
        self.ingredients = []
        self.steps = []
        self.temperature = None

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}RECIPE\n"

        if self.title:
            result += self.title.__str__(level + 1)

        if self.yield_node:
            result += self.yield_node.__str__(level + 1)

        if self.time_node:
            result += self.time_node.__str__(level + 1)

        if self.ingredients:
            result += f"{indent}  INGREDIENTS_LIST\n"
            for ingredient in self.ingredients:
                result += ingredient.__str__(level + 2)

        if self.steps:
            result += f"{indent}  STEPS_LIST\n"
            for step in self.steps:
                result += step.__str__(level + 2)

        if self.temperature:
            result += self.temperature.__str__(level + 1)

        return result
