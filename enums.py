import math
from enum import Enum

from operation import Operation


class NodeType(Enum):
    CONSTANT = 0
    OPERATION = 1
    VARIABLE = 2


ADDITION = Operation("ADDITION", 2)
SUBTRACTION = Operation("SUBTRACTION", 2)
MULTIPLICATION = Operation("MULTIPLICATION", 2)
DIVISION = Operation("DIVISION", 2)
NEGATION = Operation("NEGATION", 1)
POWER = Operation("POWER", 2)
NATURAL_LOGARITHM = Operation("LN", 1)
COSINUS = Operation("COS", 1)
SINUS = Operation("SIN", 1)


def token_to_enum(token: str) -> (NodeType, Operation | int):
    match token:
        case "+":
            _type, value = NodeType.OPERATION, ADDITION
        case "*":
            _type, value = NodeType.OPERATION, MULTIPLICATION
        case "-":
            _type, value = NodeType.OPERATION, NEGATION
        case "/":
            _type, value = NodeType.OPERATION, DIVISION
        case "^":
            _type, value = NodeType.OPERATION, POWER
        case "ln":
            _type, value = NodeType.OPERATION, NATURAL_LOGARITHM
        case "x":
            _type, value = NodeType.VARIABLE, None
        case "e":
            _type, value = NodeType.CONSTANT, math.e
        case "pi":
            _type, value = NodeType.CONSTANT, math.pi
        case "cos":
            _type, value = NodeType.OPERATION, COSINUS
        case "sin":
            _type, value = NodeType.OPERATION, SINUS
        case _:
            if token.isnumeric():
                _type, value = NodeType.CONSTANT, float(token)
            else:
                return None, None
    return _type, value
