from Lab6.src.AST import ASTNode


class StepNode(ASTNode):

    def __init__(self, instruction):
        self.instruction = instruction

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}STEP\n"
        result += f"{indent}  instruction\n"
        result += self.instruction.__str__(level + 2)
        return result