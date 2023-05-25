import function


def parse_terms(expression):
    if expression[0] not in ['-', '+']:
        expression = '+' + expression
    terms = []
    start = 0
    current = 1
    counter = 0
    while (current < len(expression)):
        if expression[current] == '{':
            counter += 1
        elif expression[current] == '}':
            counter -= 1
        elif expression[current] in ['+', '-'] and counter == 0:
            terms.append(expression[start:current])
            start = current
        current += 1
    terms.append(expression[start:])
    return terms


def parse_functions(term):
    current = 1
    while term[current].isdigit() or term.current == '.':
        current += 1
    const = float(term[:current])
    functions = []
    f = function.Function()
    while current < len(term):
        if term[current] == 'x':
            f.base = 'x'
            f.func = 'pow'
            current += 1
        elif term[current] == '{':
            f.base, current = _select_under_brackets(term, current)
            f.func = 'pow'
        elif term[current] == '\\':
            f.func, current = _define_elementary_function(term, current)
        else:
            current += 1
            continue
        if term[current] == '^':
            pass
        else:
            if f.func == 'pow':
                f.arg = 1
            else:
                f.base, f.arg, current = _define_function_args(term, f.func, current)
        functions.append(f)
        f = function.Function()
    return const, functions


def _select_under_brackets(expression, current):
    current += 1
    start = current
    counter = 0
    while expression[current] != '}' or counter > 0:
        if expression[current] == '{':
            counter += 1
        elif expression[current] == '}':
            counter -= 1
        current += 1
    key = expression[start:current]
    current += 1
    return key, current


def _define_elementary_function(expression, current):
    current += 1
    start = current
    while expression[current].isletter():
        current += 1
    func = expression[start:current]
    return func, current  


def _define_function_args(expression, func, current):
    pass
