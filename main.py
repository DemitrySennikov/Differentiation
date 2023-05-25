from syntax import syntax_checking
from derivative import take_derivative


def main():
    print("Write your expression (or print Enter to end program):")
    expression = input()
    if expression == '':
        return
    syntax_checking(expression)
    expression.replace(' ', '')
    expression.replace(',', '.')
    expression.replace('(', '{')
    expression.replace(')', '}')
    d = take_derivative(expression)
    print('Derivate:\n', d)
    main()


if __name__ == '__main__':
    main()
