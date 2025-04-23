from Lab6.src.AST import ASTNode


class IdentifierNode(ASTNode):

    def __init__(self, name):
        self.name = name

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}: {self.name}\n"
