import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from expression_tree import *

_constant = lambda x: ExpressionTreeNode(NodeType.CONSTANT, x, [])
_variable = lambda _var: ExpressionTreeNode(NodeType.VARIABLE, _var, [])

basic_expression = ExpressionTreeNode(NodeType.OPERATION,
                                      POWER,
                                      [_variable("x"), _constant(2)])

basic_expression = ExpressionTreeNode(NodeType.OPERATION, MULTIPLICATION,
                                      [_constant(3), basic_expression])

result = basic_expression.differentiate(True)


def test_differentiate():
    _test_basic_differentiation()
    _test_partial_differentiation()
    _test_difficult_differentiation()


def _test_basic_differentiation():
    _result = basic_expression.differentiate(True)
    assert str(_result) == "(3 * (2 * x))"


def test_equals():
    assert basic_expression.differentiate(True) == ExpressionTreeNode(
        NodeType.OPERATION,
        MULTIPLICATION,
        [_constant(3),
         ExpressionTreeNode(
             NodeType.OPERATION,
             MULTIPLICATION,
             [_constant(2), _variable("x")])])


def _test_partial_differentiation():
    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    POWER,
                                    [_variable("y"), _constant(2)])

    expression = ExpressionTreeNode(NodeType.OPERATION, MULTIPLICATION,
                                    [_constant(3), expression])

    expression = ExpressionTreeNode(NodeType.OPERATION, ADDITION,
                                    [expression,
                                     ExpressionTreeNode(NodeType.OPERATION,
                                                        MULTIPLICATION,
                                                        [_variable("y"),
                                                         _variable("z")])])

    _result = expression.differentiate(True, "y")
    assert str(_result) == "((3 * (2 * y)) + z)"


def _test_difficult_differentiation():
    cos_ln_sin_x = ExpressionTreeNode(NodeType.OPERATION,
                                      COSINUS,
                                      [ExpressionTreeNode(
                                          NodeType.OPERATION,
                                          NATURAL_LOGARITHM,
                                          [
                                              ExpressionTreeNode(
                                                  NodeType.OPERATION,
                                                  SINUS,
                                                  [_variable("x")])])])
    expression = ExpressionTreeNode(NodeType.OPERATION, NEGATION,
                                    [basic_expression])
    expression = ExpressionTreeNode(NodeType.OPERATION, DIVISION,
                                    [_constant(1), expression])
    expression = ExpressionTreeNode(NodeType.OPERATION, MULTIPLICATION,
                                    [expression, cos_ln_sin_x])
    print(expression)

    _result = expression.differentiate(True, "x")
    print(str(_result))
    assert str(_result) == "(((-(- * (3 * (2 * x))) / (-(3 * (x ^ 2)) * " \
                           "-(3 * (x ^ 2)))) * cos(ln(sin(x)))) + " \
                           "((1 / -(3 * (x ^ 2))) * (-sin(ln(sin(x))) * " \
                           "((1 / sin(x)) * cos(x)))))"


def test_str():
    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    NATURAL_LOGARITHM,
                                    [_variable("x")])
    assert str(expression) == "ln(x)"

    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    ADDITION,
                                    [_variable("y"), _variable("x")])
    assert str(expression) == "(y + x)"


def test_reduce():
    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    ADDITION,
                                    [_variable("x"), _variable("x")])
    assert (expression.reduce()) == ExpressionTreeNode(NodeType.OPERATION,
                                                       MULTIPLICATION,
                                                       [_constant(2),
                                                        _variable("x")])

    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    ADDITION,
                                    [_constant(1), _constant(1)])
    assert expression.reduce() == _constant(2)

    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    MULTIPLICATION,
                                    [_constant(1), _constant(1)])
    assert expression.reduce() == _constant(1)
