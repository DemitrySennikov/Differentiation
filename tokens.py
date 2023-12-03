BINARY_TOKENS = {'+', '/', '*', '^'}

TRIGONOMETRY_TOKENS = {'sin', 'cos', 'tg', 'ctg', 'arcsin', 'arccos', 'arctg',
                       'arcctg'}
LOGARITHM_TOKENS = {'ln', 'lg'}
FUNCTION_TOKENS = {*TRIGONOMETRY_TOKENS, *LOGARITHM_TOKENS}

UNARY_TOKENS = {'-', *FUNCTION_TOKENS}

CONSTANTS = {'pi', 'e'}

TOKENS = {*UNARY_TOKENS, *BINARY_TOKENS, *CONSTANTS, 'x', '(', ')'}
