import graphviz

from Lab6.src.IdentifierNode import IdentifierNode
from Lab6.src.IngredientNode import IngredientNode
from Lab6.src.NumberNode import NumberNode
from Lab6.src.RecipeNode import RecipeNode
from Lab6.src.StepNode import StepNode
from Lab6.src.StringNode import StringNode
from Lab6.src.TemperatureNode import TemperatureNode
from Lab6.src.TimeNode import TimeNode
from Lab6.src.TitleNode import TitleNode
from Lab6.src.UnitNode import UnitNode
from Lab6.src.YieldNode import YieldNode


class ASTVisualizer:

    def __init__(self):
        self.dot = graphviz.Digraph(comment='Recipe AST')
        self.node_count = 0

    def get_node_id(self):
        self.node_count += 1
        return f"node{self.node_count}"

    def visualize(self, node):
        self._add_node(node)
        return self.dot

    def _add_node(self, node, parent_id=None):
        if node is None:
            return None

        node_id = self.get_node_id()

        if isinstance(node, RecipeNode):
            self.dot.node(node_id, 'RECIPE')

            if node.title:
                title_id = self._add_node(node.title, node_id)
                self.dot.edge(node_id, title_id, label='title')

            if node.yield_node:
                yield_id = self._add_node(node.yield_node, node_id)
                self.dot.edge(node_id, yield_id, label='yield')

            if node.time_node:
                time_id = self._add_node(node.time_node, node_id)
                self.dot.edge(node_id, time_id, label='time')

            if node.ingredients:
                ingredients_id = self.get_node_id()
                self.dot.node(ingredients_id, 'INGREDIENTS_LIST')
                self.dot.edge(node_id, ingredients_id, label='ingredients')

                for ingredient in node.ingredients:
                    ing_id = self._add_node(ingredient, ingredients_id)
                    self.dot.edge(ingredients_id, ing_id)

            if node.steps:
                steps_id = self.get_node_id()
                self.dot.node(steps_id, 'STEPS_LIST')
                self.dot.edge(node_id, steps_id, label='steps')

                for step in node.steps:
                    step_id = self._add_node(step, steps_id)
                    self.dot.edge(steps_id, step_id)

            if node.temperature:
                temp_id = self._add_node(node.temperature, node_id)
                self.dot.edge(node_id, temp_id, label='temperature')

        elif isinstance(node, TitleNode):
            self.dot.node(node_id, 'TITLE')
            title_value_id = self._add_node(node.title, node_id)
            self.dot.edge(node_id, title_value_id, label='value')

        elif isinstance(node, YieldNode):
            self.dot.node(node_id, 'YIELD')
            servings_id = self._add_node(node.servings, node_id)
            self.dot.edge(node_id, servings_id, label='servings')

        elif isinstance(node, TimeNode):
            self.dot.node(node_id, 'TIME')
            duration_id = self._add_node(node.duration, node_id)
            self.dot.edge(node_id, duration_id, label='duration')
            unit_id = self._add_node(node.unit, node_id)
            self.dot.edge(node_id, unit_id, label='unit')

        elif isinstance(node, IngredientNode):
            self.dot.node(node_id, 'INGREDIENT')
            quantity_id = self._add_node(node.quantity, node_id)
            self.dot.edge(node_id, quantity_id, label='quantity')

            if node.unit:
                unit_id = self._add_node(node.unit, node_id)
                self.dot.edge(node_id, unit_id, label='unit')

            name_id = self._add_node(node.name, node_id)
            self.dot.edge(node_id, name_id, label='name')

        elif isinstance(node, StepNode):
            self.dot.node(node_id, 'STEP')
            instruction_id = self._add_node(node.instruction, node_id)
            self.dot.edge(node_id, instruction_id, label='instruction')

        elif isinstance(node, TemperatureNode):
            self.dot.node(node_id, 'TEMPERATURE')
            value_id = self._add_node(node.value, node_id)
            self.dot.edge(node_id, value_id, label='value')
            unit_id = self._add_node(node.unit, node_id)
            self.dot.edge(node_id, unit_id, label='unit')

        elif isinstance(node, NumberNode):
            self.dot.node(node_id, f'NUMBER: {node.value}')

        elif isinstance(node, StringNode):
            display_value = node.value
            if len(display_value) > 20:
                display_value = display_value[:17] + "..."
            self.dot.node(node_id, f'STRING: "{display_value}"')

        elif isinstance(node, UnitNode):
            self.dot.node(node_id, f'UNIT: {node.value}')

        elif isinstance(node, IdentifierNode):
            self.dot.node(node_id, f'ID: {node.name}')

        return node_id
