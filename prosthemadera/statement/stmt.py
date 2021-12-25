from abc import ABCMeta, abstractmethod
from typing import Union

from prosthemadera.statement.variable import IVariable


class IStmt(metaclass=ABCMeta):
    @abstractmethod
    def text(self) -> str:
        raise NotImplementedError


class Stmts(IStmt):
    children: list[IStmt]

    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def text(self) -> str:
        return ''.join([child.text() for child in self.children])

    def __add__(self, other: Union[IStmt, str]):
        if isinstance(other, Stmts):
            return Stmts(self.children + other.children)
        elif isinstance(other, str):
            return Stmts(self.children + [String(other)])
        else:
            return Stmts(self.children + [other])


class String(IStmt):
    value: str

    def __init__(self, value: str):
        self.value = value

    def text(self) -> str:
        return self.value


class FormatStmt(IStmt):
    format: str
    variables_args: tuple[IStmt]
    variables_kwargs: dict[str, IStmt]

    def __init__(self, fmt: str, *variables_args: IStmt, **variables_kwargs: IStmt):
        self.format = fmt
        self.variables_args = variables_args
        self.variables_kwargs = variables_kwargs

    def text(self) -> str:
        args = [variable.text() for variable in self.variables_args]
        kwargs = {key: variable.text() for key, variable in self.variables_kwargs.items()}
        return self.format.format(*args, **kwargs)
