from Lab6.src.ASTVisualizer import ASTVisualizer


def visualize_ast(ast):
    visualizer = ASTVisualizer()
    dot = visualizer.visualize(ast)

    try:
        dot.render('../files/recipe_ast', format='png', cleanup=True)
        print("AST visualization saved as 'files/recipe_ast.png'")
    except Exception as e:
        print(f"Could not render graph: {e}")
        print("To use visualization, install graphviz: pip install graphviz")
        print("And ensure the Graphviz binaries are in your PATH")