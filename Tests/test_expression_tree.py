import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from expression_tree import *

_constant = lambda x: ExpressionTreeNode(NodeType.CONSTANT, x, [])
_variable = lambda _var: ExpressionTreeNode(NodeType.VARIABLE, _var, [])


def test_basic_differentiation():
    expression = ExpressionTreeNode(NodeType.OPERATION,
                                    POWER,
                                    [_variable(), _constant(2)])

    expression = ExpressionTreeNode(NodeType.OPERATION, MULTIPLICATION,
                                    [_constant(3), expression])

    result = expression.differentiate(True)
    assert str(result) == "(3 * (2 * x))"
    assert result == ExpressionTreeNode(NodeType.OPERATION,
                                        MULTIPLICATION,
                                        [_constant(3),
                                         ExpressionTreeNode(
                                             NodeType.OPERATION,
                                             MULTIPLICATION,
                                             [_constant(2), _variable()])])
