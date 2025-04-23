from Lab6.src.AST import ASTNode


class LiteralNode(ASTNode):

    def __init__(self, value):
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}: {self.value}\n"