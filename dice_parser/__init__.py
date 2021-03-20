from lark import Lark
from typing import Tuple
from .transformer import FormulaTransformer
from . import data_model


def _init_parser():
    # Assume working directory is the project root.
    with open("dice_parser/dice_formula.lark", 'r') as lark_file:
        return Lark(lark_file, parser="lalr")


_parser = _init_parser()

_formula_transformer = FormulaTransformer()


def print_tree(formula: str) -> None:
    tree = _parser.parse(formula)
    print(tree.pretty())


def reprint_formula(formula: str) -> None:
    tree = _parser.parse(formula)
    print(_formula_transformer.transform(tree))


class RollResults:
    def __init__(self, data: data_model.Value):
        # We need to save how the formula looks every step of the way.
        self.original = str(data)
        # Roll the dice...
        data = data_model.ensure_partial_eval(data)
        self.rolled = str(data)
        # Sum it up.
        self.result = data_model.ensure_int(data)

    def __str__(self):
        return f"RollResults{{original: {self.original}, rolled: {self.rolled}, result: {self.result}}}"


def parse_and_roll(formula: str) -> RollResults:
    tree = _parser.parse(formula)
    data = _formula_transformer.transform(tree)
    return RollResults(data)
