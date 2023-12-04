BINARY_TOKENS = {'+', '/', '*', '^'}

FUNCTION_TOKENS = {'sin', 'cos', 'ln'}
FUNCTION_TOKENS = {'sin', 'cos', 'ln'}

UNARY_TOKENS = {'-', *FUNCTION_TOKENS}

VARIABLE_TOKENS = {'x', 'y', 'z'}

VARIABLE_TOKENS = {'x', 'y', 'z'}

CONSTANTS = {'pi', 'e'}

TOKENS = {*UNARY_TOKENS, *BINARY_TOKENS, *CONSTANTS,
          *VARIABLE_TOKENS, '(', ')'}
