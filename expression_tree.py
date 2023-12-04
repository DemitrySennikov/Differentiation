from __future__ import annotations

from numbers import Number

from enums import *
from operation import Operation


class ExpressionTreeNode:
    def __init__(self, node_type: NodeType,
                 node_value: None | str | isinstance(Number ) | isinstance(
                     Operation) = None,
                 arguments: list[ExpressionTreeNode] = ()):

        self._parent = None

        self._type = node_type

        self._validate_value()
        self._value = node_value

        self._validate_arguments()
        self._arguments = arguments

        for node in arguments:
            node._parent = self

    def _validate_value(self):
        return

    def _validate_arguments(self):
        return

    def is_constant(self, constant):
        if not self._type == NodeType.CONSTANT:
            return False
        return self._value == constant

    def _is_variable(self, variable):
        return self._type == NodeType.VARIABLE and self._value == variable

    def differentiate(self, should_reduce: bool = False,
                      variable: str = "x") -> ExpressionTreeNode:
        if self._type == NodeType.CONSTANT:
            return ExpressionTreeNode(NodeType.CONSTANT, 0)
        if self._type == NodeType.VARIABLE:
            if self._is_variable(variable):
                return ExpressionTreeNode(NodeType.CONSTANT, 1)
            return ExpressionTreeNode(NodeType.CONSTANT, 0)

        name = self._value.name
        arity = self._value.arity

        result = None
        if arity == 1:
            operand = self._arguments[0]
            match name:
                case "NEGATION":
                    outer_derivative = ExpressionTreeNode(NodeType.CONSTANT,
                                                          "-")
                case "LN":
                    outer_derivative = _divide(_constant(1), operand)
                case "COS":
                    outer_derivative = _neg(_sin(operand))
                case "SIN":
                    outer_derivative = _cos(operand)
                case _:
                    raise ValueError("Wrong operation!")
            result = _multiply(outer_derivative,
                               operand.differentiate(should_reduce, variable))

        if arity == 2:
            first, second = self._arguments[0], self._arguments[1]
            match self._value.name:
                case "ADDITION":
                    result = _add(first.differentiate(should_reduce, variable),
                                  second.differentiate(should_reduce,
                                                       variable))
                case "MULTIPLICATION":
                    first_term = _multiply(
                        first.differentiate(should_reduce, variable),
                        second)
                    second_term = _multiply(first,
                                            second.differentiate(should_reduce,
                                                                 variable))

                    result = _add(first_term, second_term)
                case "SUBTRACTION":
                    result = _subtract(
                        first.differentiate(should_reduce, variable),
                        second.differentiate(should_reduce, variable))
                case "DIVISION":
                    first_term_of_numerator = _multiply(
                        first.differentiate(should_reduce, variable),
                        second)
                    second_term_of_numerator = _multiply(
                        first,
                        second.differentiate(should_reduce, variable))

                    numerator = _subtract(first_term_of_numerator,
                                          second_term_of_numerator)

                    denominator = _multiply(second, second)
                    result = _divide(numerator, denominator)
                case "POWER":
                    if self._arguments[0].is_constant(math.e):
                        result = _multiply(self,
                                           self._arguments[1].differentiate(
                                               should_reduce, variable))
                    elif self._arguments[0]._is_variable(variable) \
                            and self._arguments[1]._type == NodeType.CONSTANT:
                        _power_number = self._arguments[1]._value
                        result = _multiply(_constant(_power_number),
                                           _power(_variable(variable),
                                                  _constant(
                                                      _power_number - 1)))

                    else:
                        argument = _multiply(self._arguments[1],
                                             _ln(self._arguments[0]))
                        outer = _power(_constant(math.e), argument)
                        inner = argument.differentiate(should_reduce, variable)
                        result = _multiply(outer, inner)
                case _:
                    raise ValueError("Wrong operation!")
        if should_reduce:
            return result.reduce()
        return result

    def __eq__(self, other: ExpressionTreeNode):
        if not self:
            if not other:
                return True
            return False
        other_value = other._value
        self_value = self._value
        if self._type is not other._type:
            return False
        _type = self._type
        if _type == NodeType.CONSTANT:
            return self_value == other_value
        if _type == NodeType.VARIABLE:
            return self_value == other_value
        if _type == NodeType.OPERATION:
            if self._value.name != other._value.name:
                return False
        if len(self._arguments) != len(other._arguments):
            return False
        result = True
        for self_argument, other_argument in tuple(
                zip(self._arguments, other._arguments)):
            result &= self_argument == other_argument
        return result

    def reduce(self):
        result = self
        for i in range(5):
            result = result._reduce()

        return result

    def _reduce(self):
        self._arguments = [node._reduce() for node in self._arguments]

        result = self
        result = result._reduce_simple_constants()
        result = result._reduce_simple_operations()
        result = result._constants_to_left()
        result = result._reduce_operations_with_constants()

        return result

    def _constants_to_left(self):
        if self._type != NodeType.OPERATION:
            return self
        if self._value.name == "ADDITION" \
                or self._value.name == "MULTIPLICATION":
            if self._arguments[1]._type == NodeType.CONSTANT:
                self._arguments[0], self._arguments[1] = \
                    self._arguments[1], self._arguments[0]
        return self

    def _reduce_simple_operations(self):
        if self._type != NodeType.OPERATION:
            return self

        match self._value.name:
            case "ADDITION":
                if self._arguments[0] == self._arguments[1]:
                    return _multiply(_constant(2), self._arguments[0])

        return self

    def _reduce_operations_with_constants(self):
        if self._type != NodeType.OPERATION:
            return self
        for argument in self._arguments:
            if argument._type != NodeType.CONSTANT:
                return self
        if self._value.arity != 2:
            return self
        a, b = float(self._arguments[0]._value), \
            float(self._arguments[1]._value)

        match self._value.name:
            case "ADDITION":
                return _constant(a + b)
            case "MULTIPLICATION":
                return _constant(a * b)
        return self

    def _reduce_simple_constants(self):
        if self._type != NodeType.OPERATION:
            return self

        non_zero_arguments = list(
            filter(lambda node: node and not node.is_constant(0),
                   self._arguments)
        )

        non_one_arguments = list(
            filter(lambda node: node and not node.is_constant(1),
                   self._arguments)
        )

        match self._value.name:
            case "ADDITION":
                if len(non_zero_arguments) == 0:
                    return _constant(0)
                if len(non_zero_arguments) == 1:
                    return non_zero_arguments[0]
            case "MULTIPLICATION":
                if len(non_zero_arguments) < len(self._arguments):
                    return _constant(0)
                if len(non_one_arguments) == 1:
                    return non_one_arguments[0]
            case "DIVISION":
                if self._arguments[1].is_constant(0):
                    raise ZeroDivisionError
                if self._arguments[0].is_constant(0):
                    return _constant(0)
            case "SUBTRACTION":
                if self._arguments[1].is_constant(0):
                    return self._arguments[0]
                if self._arguments[0].is_constant(0):
                    return ExpressionTreeNode(NodeType.OPERATION,
                                              NEGATION,
                                              [self._arguments[1]])
            case "NEGATION":
                if self._arguments[0].is_constant(0):
                    return _constant(-self._arguments[0]._value)
            case "POWER":
                if self._arguments[1].is_constant(0):
                    return _constant(1)
                if self._arguments[1].is_constant(1):
                    return self._arguments[0]

        return self

    def __str__(self):
        match self._type:
            case NodeType.VARIABLE:
                return self._value
            case NodeType.CONSTANT:
                if self._value == math.e:
                    return "e"
                if self._value == math.pi:
                    return "pi"
                return str(self._value)
            case NodeType.OPERATION:
                match self._value.arity:
                    case 1:
                        if self._value.name == "NEGATION":
                            return f"-{self._arguments[0]}"
                        elif self._value.name == "LN":
                            return f"ln({self._arguments[0]})"
                        elif self._value.name == "SIN":
                            return f"sin({self._arguments[0]})"
                        elif self._value.name == "COS":
                            return f"cos({self._arguments[0]})"
                        else:
                            raise NotImplementedError
                    case 2:
                        string_reprs = {
                            "ADDITION": "+",
                            "SUBTRACTION": "-",
                            "DIVISION": "/",
                            "MULTIPLICATION": "*",
                            "POWER": "^"
                        }
                        if self._value.name in string_reprs:
                            return f"({self._arguments[0]} " \
                                   f"{string_reprs[self._value.name]} " \
                                   f"{self._arguments[1]})"
                    case _:
                        raise NotImplementedError


def _unary_operation(operand: ExpressionTreeNode,
                     operation: Operation) -> ExpressionTreeNode:
    return ExpressionTreeNode(NodeType.OPERATION,
                              operation,
                              [operand])


def _binary_operation(first: ExpressionTreeNode,
                      second: ExpressionTreeNode,
                      operation: Operation) -> ExpressionTreeNode:
    return ExpressionTreeNode(NodeType.OPERATION,
                              operation,
                              [first, second])


_add = lambda first, second: _binary_operation(first, second,
                                               ADDITION)

_multiply = lambda first, second: \
    _binary_operation(first, second, MULTIPLICATION)

_subtract = lambda first, second: \
    _binary_operation(first, second, SUBTRACTION)

_divide = lambda first, second: \
    _binary_operation(first, second, DIVISION)

_power = lambda first, second: \
    _binary_operation(first, second, POWER)

_constant = lambda constant: ExpressionTreeNode(NodeType.CONSTANT,
                                                constant)

_ln = lambda argument: _unary_operation(argument, NATURAL_LOGARITHM)
_sin = lambda argument: _unary_operation(argument, SINUS)
_cos = lambda argument: _unary_operation(argument, COSINUS)
_neg = lambda argument: _unary_operation(argument, NEGATION)

_variable = lambda var: ExpressionTreeNode(NodeType.VARIABLE, var, [])
