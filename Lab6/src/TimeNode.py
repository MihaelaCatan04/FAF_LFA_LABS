from Lab6.src.AST import ASTNode


class TimeNode(ASTNode):

    def __init__(self, duration, unit):
        self.duration = duration
        self.unit = unit

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}TIME\n"
        result += f"{indent}  duration\n"
        result += self.duration.__str__(level + 2)
        result += f"{indent}  unit\n"
        result += self.unit.__str__(level + 2)
        return result