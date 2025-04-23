from Lab6.src.AST import ASTNode


class TitleNode(ASTNode):

    def __init__(self, title):
        self.title = title

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}TITLE\n"
        result += self.title.__str__(level + 1)
        return result