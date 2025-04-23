class ASTNode:

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}\n"

    def visualize(self):
        print(self.__str__())