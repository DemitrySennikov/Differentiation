import tokenizer
from tokens import FUNCTION_TOKENS


def parse(expression: str):
    expression.replace(',', '.')
    expression.replace(" ", "")
    expression_tokens = tokenizer.create_tokens(expression)
    tokenizer.is_correct_brackets(expression_tokens)
    tokenizer.is_correct_operations(expression_tokens)
    return expression, [token[0] for token in _parse(expression_tokens, [])]


def _parse(exp_tokens: list, order: list):
    terms, term_operations = _parse_terms(exp_tokens)
    first_term_neg_token = None
    if len(terms) == len(term_operations):
        first_term_neg_token = term_operations.pop(0)
    for term_index in range(len(terms)):
        multipliers, mul_operations = _parse_multipliers(terms[term_index])
        for multiplier_index in range(len(multipliers)):
            arguments, pow_operations = _parse_powers(
                multipliers[multiplier_index])
            for argument in arguments:
                if argument[0][0] == '(':
                    order = _parse(argument[1:len(argument) - 1], order)
                elif argument[0][0] in FUNCTION_TOKENS:
                    if argument[1][0] == '(':
                        order = _parse(argument[2:len(argument) - 1], order)
                    else:
                        order.append(argument[1])
                    order.append(argument[0])
                else:
                    order.append(*argument)
            order.extend(pow_operations[::-1])
            if multiplier_index > 0:
                order.append(mul_operations[multiplier_index - 1])
        if term_index > 0:
            order.append(term_operations[term_index - 1])
            if term_operations[term_index - 1][0] == '-':
                order.append(('+', term_operations[term_index - 1][1]))
        elif first_term_neg_token is not None:
            order.append(first_term_neg_token)
    return order


def _parse_powers(multipliers_tokens: list):
    arguments = []
    operations = []
    i = 0
    while i < len(multipliers_tokens):
        argument = []
        if multipliers_tokens[i][0] == '(':
            expression, i = _bracket_expression(multipliers_tokens, i)
            arguments.append(expression)
        elif multipliers_tokens[i][0] in FUNCTION_TOKENS:
            argument.append(multipliers_tokens[i])
            i += 1
            if multipliers_tokens[i][0] == '(':
                expression, i = _bracket_expression(multipliers_tokens, i)
                argument.extend(expression)
            else:
                argument.append(multipliers_tokens[i])
            arguments.append(argument)
        else:
            arguments.append([multipliers_tokens[i]])
        i += 1
        if i < len(multipliers_tokens):
            operations.append(multipliers_tokens[i])
            i += 1
    return arguments, operations


def _parse_multipliers(term_tokens: list):
    multipliers = []
    operations = []
    i = 0
    while i < len(term_tokens):
        multiplier = []
        if term_tokens[i][0] == '(':
            expr, i = _bracket_expression(term_tokens, i)
            multiplier.extend(expr)
        elif term_tokens[i][0] in FUNCTION_TOKENS:
            multiplier.append(term_tokens[i])
            i += 1
            if term_tokens[i][0] == '(':
                expr, i = _bracket_expression(term_tokens, i)
                multiplier.extend(expr)
            else:
                multiplier.append(term_tokens[i])
        else:
            multiplier.append(term_tokens[i])
        i += 1
        if i < len(term_tokens) and term_tokens[i][0] == '^':
            multiplier.append(term_tokens[i])
            i += 1
            if term_tokens[i][0] == '(':
                expr, i = _bracket_expression(term_tokens, i)
                multiplier.extend(expr)
            else:
                multiplier.append(term_tokens[i])
            i += 1
        if i < len(term_tokens):
            if term_tokens[i][0] in ['*', '/']:
                operations.append(term_tokens[i])
                i += 1
            else:
                operations.append(('*', term_tokens[i][1]))
        multipliers.append(multiplier)
    return multipliers, operations


def _parse_terms(expression_tokens: list):
    terms = []
    operations = []
    i = 0
    if expression_tokens[0][0] == '-':
        operations.append(expression_tokens[0])
        i = 1
    while i < len(expression_tokens):
        term = []
        while expression_tokens[i][0] not in ['+', '-']:
            if expression_tokens[i][0] == '(':
                expr, i = _bracket_expression(expression_tokens, i)
                term.extend(expr)
            else:
                term.append(expression_tokens[i])
            i += 1
            if i == len(expression_tokens):
                break
        if i < len(expression_tokens):
            operations.append(expression_tokens[i])
        terms.append(term)
        i += 1
    return terms, operations


def _bracket_expression(expression_tokens: list, index: int):
    counter = 1
    expression = [expression_tokens[index]]
    while counter > 0:
        index += 1
        expression.append(expression_tokens[index])
        if expression_tokens[index][0] == '(':
            counter += 1
        if expression_tokens[index][0] == ')':
            counter -= 1
    return expression, index
