from abc import ABC, abstractmethod
from typing import TypeVar, Generic

ExecutorInputType = TypeVar('ExecutorInputType')
ExecutorOutputType = TypeVar('ExecutorOutputType')
ExecutionContextType = TypeVar('ExecutionContextType')


class CodeExecutionStrategy(ABC, Generic[ExecutionContextType, ExecutorInputType, ExecutorOutputType]):
    def execute_code(self, execution_context: ExecutionContextType, input: ExecutorInputType) -> ExecutorOutputType:
        return self._execute(execution_context, input)

    @abstractmethod
    def _execute(self, execution_context: ExecutionContextType, input: ExecutorInputType) -> ExecutorOutputType:
        pass
