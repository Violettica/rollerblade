from abc import ABC, abstractmethod
from typing import Union, Callable, List
from enum import Enum, auto
import random

rng = random.SystemRandom()


class Evaluable(ABC):
    @abstractmethod
    def eval(self) -> int:
        ...

    @abstractmethod
    def partial_eval(self) -> 'Evaluable':
        ...


Value = Union[int, Evaluable]


def ensure_int(value: Value) -> int:
    if type(value) is int:
        return value
    else:
        # Must be an Evaluable, then.
        return value.eval()


def ensure_partial_eval(value: Value) -> Value:
    try:
        return value.partial_eval()
    except AttributeError:
        # Must be an int
        return value


class SpecialDie(Enum):
    FATE = auto

    def __str__(self):
        if self == self.FATE:
            return 'F'
        else:
            raise NotImplementedError("This special die type lacks a formatter!")


Die = Union[int, SpecialDie]


class Dice(Evaluable):
    def __init__(self, num_dice: int, die: Die):
        self.num_dice = num_dice
        self.die = die

    def roll(self) -> List[int]:
        if type(self.die) is int:
            start, end = 1, self.die
        elif self.die == SpecialDie.FATE:
            start, end = -1, 1
        else:
            raise NotImplementedError("This special die lacks rolling support!")

        return [rng.randint(start, end) for _ in range(self.num_dice)]

    def partial_eval(self) -> 'Evaluable':
        return RolledDice(self)

    def eval(self) -> int:
        return sum(self.roll())

    def __str__(self):
        return f"`{self.num_dice}d{self.die}`"


class RolledDice(Evaluable):
    def __init__(self, dice: Dice):
        self.results = dice.roll()
        self.die = dice.die

    def partial_eval(self) -> 'Evaluable':
        return self

    def eval(self) -> int:
        return sum(self.results)

    def __str__(self):
        if type(self.die) is int:
            printout = "+".join(map(lambda x: str(x), self.results))
        elif self.die == SpecialDie.FATE:
            def fate_mapping(num: int) -> str:
                if num == 0:
                    return 'b'
                elif num == 1:
                    return '+'
                else:  # Must be -1
                    return '-'

            printout = "".join(map(fate_mapping, self.results))
        else:
            raise NotImplementedError("Special die partial eval formatting not supported!")

        return f"`{printout}`"


class UnaryOperator:
    def __init__(self, symbol: str, function: Callable[[int], int]):
        self.symbol = symbol
        self.function = function

    def perform(self, val: int) -> int:
        return self.function(val)

    def __str__(self):
        return self.symbol


class UnaryOperation(Evaluable):
    def __init__(self, val: Value, operation: UnaryOperator, enclosed: bool = False):
        self.val = val
        self.operation = operation
        self.enclosed = enclosed

    def eval(self) -> int:
        return self.operation.perform(ensure_int(self.val))

    def partial_eval(self) -> 'Evaluable':
        self.val = ensure_partial_eval(self.val)
        return self

    def __str__(self):
        basis = f"{self.operation.symbol}{self.val}"

        if self.enclosed:
            return f"({basis})"
        else:
            return basis


class BinaryOperator:
    def __init__(self, symbol: str, function: Callable[[int, int], int]):
        self.symbol = symbol
        self.function = function

    def perform(self, left: int, right: int) -> int:
        return self.function(left, right)

    def __str__(self):
        return self.symbol


class BinaryOperation(Evaluable):
    def __init__(self, left: Value, right: Value, operation: BinaryOperator, enclosed: bool = False):
        self.left = left
        self.right = right
        self.operation = operation
        self.enclosed = enclosed

    def eval(self) -> int:
        int_left, int_right = ensure_int(self.left), ensure_int(self.right)
        return self.operation.perform(int_left, int_right)

    def partial_eval(self) -> 'Evaluable':
        self.left, self.right = ensure_partial_eval(self.left), ensure_partial_eval(self.right)
        return self

    def __str__(self):
        basis = f"{self.left} {self.operation.symbol} {self.right}"
        if self.enclosed:
            return f"({basis})"
        else:
            return basis



