from lark import Transformer
from .data_model import UnaryOperator, UnaryOperation, BinaryOperator, BinaryOperation, SpecialDie, Dice

_DIVISION_OPERATOR = BinaryOperator('/', lambda a, b: a // b)

_MULTIPLICATION_OPERATOR = BinaryOperator('*', lambda a, b: a * b)

_SUBTRACTION_OPERATOR = BinaryOperator('-', lambda a, b: a - b)

_ADDITION_OPERATOR = BinaryOperator('+', lambda a, b: a + b)

_NEGATION_OPERATOR = UnaryOperator('-', lambda val: -val)


class FormulaTransformer(Transformer):
    def int(self, n):
        (n,) = n
        return int(n)

    def enclosure(self, e):
        (at,) = e

        try:
            at.enclosed = True
        except TypeError or AttributeError:
            pass  # Not an Operation. Return it normally.
        finally:
            return at

    def neg(self, args):
        (val,) = args

        operator = _NEGATION_OPERATOR

        return UnaryOperation(val, operator)

    def dice(self, args):
        (num_dice, die,) = args

        # Unfortunately, our dice are possibly Token. This is a problem.
        num_dice = int(num_dice)
        try:
            die = int(die)
        except TypeError:  # This means it's probably a SpecialDie, so we can ignore this.
            # Put in an assert for good luck
            assert type(die) == SpecialDie

        return Dice(num_dice, die)

    def fate(self, _):
        return SpecialDie.FATE

    def add(self, args):
        (left, right,) = args

        operator = _ADDITION_OPERATOR

        return BinaryOperation(left, right, operator)

    def sub(self, args):
        (left, right,) = args

        operator = _SUBTRACTION_OPERATOR

        return BinaryOperation(left, right, operator)

    def mul(self, args):
        (left, right,) = args

        operator = _MULTIPLICATION_OPERATOR

        return BinaryOperation(left, right, operator)

    def div(self, args):
        (left, right,) = args

        operator = _DIVISION_OPERATOR

        return BinaryOperation(left, right, operator)