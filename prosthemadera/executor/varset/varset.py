from typing import TypeVar, Generic

T = TypeVar('T')


class VariableSet(Generic[T]):
    set: list[T]

    def __init__(self, variable_set: list[T]):
        self.set = variable_set

    def get_set(self) -> list[T]:
        return self.set
