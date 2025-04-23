from Lab6.src.AST import ASTNode


class BinaryNode(ASTNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.__class__.__name__}\n"
        result += self.left.__str__(level + 1)
        result += self.right.__str__(level + 1)
        return result
