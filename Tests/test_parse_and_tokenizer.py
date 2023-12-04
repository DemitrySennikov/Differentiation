import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from parse import parse

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.test_cases = ['54.0', '23', '423.4534', 'y', 'xyz', '23x',
                           'x+4', '-50', '2-z', 'sinx', 'ln(x+4)', 
                           '4*cospi', 'e/ln(y)', 'e^yz', 
                           '42x+(-sin(2.0x+pi)^2+8lnz)*cos(y/z)-4+zyx']
        self.answers = [('54.0', ['54.0']), ('23', ['23']), 
                        ('423.4534', ['423.4534']), ('y', ['y']), 
                        ('xyz', ['x', 'y', '*', 'z', '*']), 
                        ('23x', ['23', 'x', '*']), ('x+4', ['x', '4', '+']), 
                        ('-50', ['50', '-']), ('2-z', ['2', 'z', '-', '+']), 
                        ('sinx', ['x', 'sin']), 
                        ('ln(x+4)', ['x', '4', '+', 'ln']), 
                        ('4*cospi', ['4', 'pi', 'cos', '*']), 
                        ('e/ln(y)', ['e', 'y', 'ln', '/']), 
                        ('e^yz', ['e', 'y', '^', 'z', '*']), 
                        ('42x+(-sin(2.0x+pi)^2+8lnz)*cos(y/z)-4+zyx', 
                         ['42', 'x', '*', '2.0', 'x', '*', 'pi', '+', 'sin',
                          '2', '^', '-', '8', 'z', 'ln', '*', '+', 'y', 'z', 
                          '/', 'cos', '*', '+', '4', '-', '+', 'z', 'y', '*', 
                          'x', '*', '+'])]
        self.error_cases = ['324.', '43423.3432.234x', '.454532z', 't*x',
                            'sin()+2', '(5x*(pi+e)', 'ln x+4)', '3*(4+)',
                            '+42', '*y', '/76', 'zy-*4', '32+*', 'x*', 'ln+3', 
                            '42x+(-sin(2.0x+pi)^2+8lnz)*co(y/z)-4+zyx']

    def test_correct_cases(self):
        for i in range(len(self.test_cases)):
            self.assertEqual(parse(self.test_cases[i]), self.answers[i])
    
    def test_uncorrect_cases(self):
        for i in range(len(self.error_cases)):
            try:
                parse(self.error_cases[i])
                self.assertFalse(True, msg='Error test passed!')
            except SyntaxError:
                self.assertTrue(True)
            except ValueError:
                self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
