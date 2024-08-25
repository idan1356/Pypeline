from abc import ABC, abstractmethod
from typing import TypeVar, Generic

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


class CodeExecutionStrategy(ABC, Generic[InputType, OutputType]):
    def execute_code(self, code_str: str, input: InputType) -> OutputType:
        return self._execute(code_str, input)

    @abstractmethod
    def _execute(self, code_str: str, input: InputType) -> OutputType:
        pass
