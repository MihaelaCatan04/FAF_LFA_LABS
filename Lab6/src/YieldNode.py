from Lab6.src.AST import ASTNode


class YieldNode(ASTNode):

    def __init__(self, servings):
        self.servings = servings

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}YIELD\n"
        result += f"{indent}  servings\n"
        result += self.servings.__str__(level + 2)
        return result