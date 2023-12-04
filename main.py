import argparse

from enums import *
from expression_tree import ExpressionTreeNode
from parse import parse


def differentiate(_expression: str, _variable: str):
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
    result = str(nodes_stack.pop().differentiate(True, _variable))
    if result[0] == "(" and result[-1] == ")":
        return result[1:-1]
    return result


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog='symbolic-differentiation',
        description='This program finds the derivative of a given '
                    'function in symbolic form.')
    argparser.add_argument('function', type=str,
                           help="Function of x, y, z as a string. "
                                "Not all variables need to be used.")
    args = argparser.parse_args()
    function = args.function.replace(' ', '')
    try:
        if len(function) == 0:
            raise ValueError("Empty string.")
        variables = []
        for variable in ["x", "y", "z"]:
            if variable in function:
                variables.append(variable)
        if len(variables) == 0:
            variables.append("x")
        if len(variables) == 1:
            variable = variables[0]
            print(f"f({variable}) = {function}")
            print(f"df/d{variable} = "
                  f"{differentiate(function, variable)}")
        else:
            print(f"f({', '.join(variables)}) = {function}")
            for variable in variables:
                print(f"δf/δ{variable} = "
                      f"{differentiate(function, variable)}")
    except Exception as e:
        print(e)
