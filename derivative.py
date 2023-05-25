import func_parser as p
import function


def take_derivative(expression):
    derivative = ''
    terms = p.parse_terms(expression)
    for term in terms:
        const, functions = p.parse_functions(term)
        derivatives = _derivate_multipliable_functions(functions)
        der_term = _derivate_multiply(const, functions, derivatives)
        if der_term == '':
            continue
        if derivative == '' and der_term[0] == '+':
            der_term = der_term[1:]
        derivative += der_term
    return derivative


def _derivate_multipliable_functions(functions):
    pass


def _derivate_multiply(const, functions, derivatives):
    pass
