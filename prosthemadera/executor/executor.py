import sys
from typing import TypeVar, Generic

from prosthemadera.checker import Checker
from prosthemadera.executor.varset import Range, VariableSet
from prosthemadera.statement import Variable, IStmt, Operator

T = TypeVar('T')


class Executor:
    checker: Checker
    statement: IStmt

    def __init__(self, checker: Checker, statement: IStmt):
        self.checker = checker
        self.statement = statement

    def get_integer(self, *, variable: Variable[int]):
        now = 1
        while True:
            variable.set_value(now)
            result = self.checker.check_statement(self.statement.text())
            print(f'{now} => {result}')
            if not result:
                break
            now *= 2

        low = now // 2
        high = now
        while low + 1 < high:
            middle = (low + high) // 2
            variable.set_value(middle)
            result = self.checker.check_statement(self.statement.text())
            print(f'{middle} => {result}')
            if result:
                low = middle
            else:
                high = middle

        return low

    def get_text(self, *, length: int, index: Variable[int], comparator: Operator, variable: Variable[int],
                 variable_sets: list[VariableSet[int]]) -> str:
        text = ''
        for i in range(length):
            index.set_value(i + 1)
            text += self.get_char(
                comparator=comparator,
                variable=variable,
                variable_sets=variable_sets)
            print(text)
        return text

    def get_char(self, *, comparator: Operator, variable: Variable[int], variable_sets: list[VariableSet[int]]) -> str:
        false_ranges = []  # type: list[Range]
        for variable_set in variable_sets:
            bss = BinarySearchSet(variable_set.get_set())
            for false_range in false_ranges:
                bss.remove_range(false_range)

            while not bss.is_finish():
                middle = bss.get_middle()
                variable.set_value(middle)
                result = self.checker.check_statement(self.statement.text())
                print(f'{middle} ({chr(middle)}) => {result}')
                if result:
                    # target_value >= middle
                    false_range = Range(0, middle)
                else:
                    false_range = Range(middle, sys.maxsize)
                bss.remove_range(false_range)
                false_ranges.append(false_range)

            original = comparator.text()
            comparator.set_value('=')
            variable.set_value(bss.get_result())
            result = self.checker.check_statement(self.statement.text())
            comparator.set_value(original)
            if result:
                return chr(bss.get_result())

        raise Exception('No result')


class BinarySearchSet(Generic[T]):
    set: list[T]

    def __init__(self, variable_set: list[T]):
        self.set = variable_set
        self.set.sort()

    def get_middle(self) -> T:
        return self.set[len(self.set) // 2]

    def is_finish(self) -> bool:
        return len(self.set) == 1

    def get_result(self) -> T:
        assert self.is_finish()
        return self.set[0]

    def remove_range(self, rng: Range) -> None:
        self.set = [x for x in self.set if not rng.low <= x < rng.high]
