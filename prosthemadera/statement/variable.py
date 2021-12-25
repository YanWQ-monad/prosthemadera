from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Optional, Any, Tuple

from prosthemadera.statement.stmt import IStmt, String

T = TypeVar('T')


class IVariable(Generic[T], IStmt, metaclass=ABCMeta):
    @abstractmethod
    def set_value(self, value: Optional[T]) -> None:
        raise NotImplementedError


class Variable(IVariable[T]):
    value: Optional[T]

    def __init__(self):
        self.value = None

    def set_value(self, value: Optional[T]) -> None:
        self.value = value

    def text(self) -> str:
        if self.value is None:
            raise ValueError('Variable value is not set')
        return str(self.value)


class Operator(Variable[T]):
    def __init__(self, operator: str):
        super(Operator, self).__init__()
        self.set_value(operator)


def variables(count: int) -> tuple[Variable[Any], ...]:
    return tuple(Variable() for _ in range(count))
