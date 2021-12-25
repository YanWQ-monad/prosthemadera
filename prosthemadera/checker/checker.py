from abc import ABCMeta, abstractmethod


class Checker(metaclass=ABCMeta):
    @abstractmethod
    def check_statement(self, statement: str):
        raise NotImplementedError
