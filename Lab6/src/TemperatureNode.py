from Lab6.src.AST import ASTNode


class TemperatureNode(ASTNode):

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}TEMPERATURE\n"
        result += f"{indent}  value\n"
        result += self.value.__str__(level + 2)
        result += f"{indent}  unit\n"
        result += self.unit.__str__(level + 2)
        return result