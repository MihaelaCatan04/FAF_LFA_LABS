from Lab6.src.AST import ASTNode


class IngredientNode(ASTNode):

    def __init__(self, quantity, unit, name):
        self.quantity = quantity
        self.unit = unit
        self.name = name

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}INGREDIENT\n"
        result += f"{indent}  quantity\n"
        result += self.quantity.__str__(level + 2)

        if self.unit:
            result += f"{indent}  unit\n"
            result += self.unit.__str__(level + 2)

        result += f"{indent}  name\n"
        result += self.name.__str__(level + 2)

        return result
