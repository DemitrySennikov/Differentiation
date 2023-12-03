import argparse

from enums import *
from expression_tree import ExpressionTreeNode
from parse import parse


def differentiate(_expression: str):
    _input, expression_in_inverse_notation = parse(_expression)
    nodes_stack = []
    for symbol in expression_in_inverse_notation:
        _type, value = token_to_enum(symbol)
        if _type is None:
            raise ValueError("Wrong symbol!")
        elif _type is NodeType.OPERATION and isinstance(value, Operation):
            nodes = []
            for i in range(value.arity):
                nodes.append(nodes_stack.pop())
            nodes.reverse()
            nodes_stack.append(ExpressionTreeNode(_type, value, nodes))
        else:
            nodes_stack.append(ExpressionTreeNode(_type, value))
    result = str(nodes_stack.pop().differentiate(True))
    if result[0] == "(" and result[-1] == ")":
        return result[1:-1]
    return result


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('expression', type=str)
    args = argparser.parse_args()
    expression = args.expression
    try:
        print(f"f(x) = {expression.replace(' ', '')}")
        print(f"f'(x) = {differentiate(expression)}")
    except Exception as e:
        print(e)