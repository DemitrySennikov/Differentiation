from tokens import BINARY_TOKENS, UNARY_TOKENS, CONSTANTS
from tokens import TOKENS, VARIABLE_TOKENS
from tokens import TOKENS, VARIABLE_TOKENS


def create_tokens(expression: str):
    start = 0
    current = 1
    expression_tokens = []
    while current <= len(expression):
        s = expression[start:current]
        if s.isdigit():
            has_dot = False
            while current < len(expression):
                if expression[current] == '.':
                    if has_dot:
                        raise SyntaxError(f'{start}: Number with 2 dots')
                    has_dot = True
                    if current + 1 == len(expression):
                        raise SyntaxError(
                            f'{current}: Dot without fractional part')
                    if not expression[current+1].isdigit():
                        raise SyntaxError(
                            f'{current}: Dot without fractional part')
                elif not expression[current].isdigit():
                    break
                current += 1
            expression_tokens.append((expression[start:current], start))
            start = current
        elif s in TOKENS:
            expression_tokens.append((s, start))
            start = current
        current += 1
    if start != len(expression):
        raise SyntaxError(f'{start}: Unexpected token')
    return expression_tokens


def is_correct_brackets(expression_tokens: list):
    opened_indexes = []
    for i in range(len(expression_tokens)):
        token = expression_tokens[i]
        if token[0] == '(':
            opened_indexes.append(token[1])
        elif token[0] == ')':
            if len(opened_indexes) == 0:
                raise SyntaxError(f'{token[1]}: Not opened bracket')
            if expression_tokens[i - 1][0] == '(':
                raise ValueError(f'{token[1]}: Empty brackets')
            opened_indexes.pop()
    if len(opened_indexes) > 0:
        raise SyntaxError(f'{opened_indexes.pop()}: Not closed bracket')
    return True


def is_correct_operations(expression_tokens: list):
    for i in range(len(expression_tokens)):
        token = expression_tokens[i]
        if token[0] in BINARY_TOKENS:
            if (i == 0 or (expression_tokens[i - 1][0] not in 
                           [')', *VARIABLE_TOKENS, *CONSTANTS] and
                           not expression_tokens[i - 1][0][0].isdigit())):
                raise ValueError(
                    f'{token[1]}: Binary operation without first argument')
            if (i + 1 == len(expression_tokens) or
                    expression_tokens[i + 1][0] in [')', '-', *BINARY_TOKENS]):
                raise ValueError(
                    f'{token[1]}: Binary operation without second argument')
        elif token[0] in UNARY_TOKENS:
            if (i + 1 == len(expression_tokens) or
                    expression_tokens[i + 1][0] in [')', '-', *BINARY_TOKENS]):
                raise ValueError(
                    f'{token[1]}: Unary operation without argument')
    return True

