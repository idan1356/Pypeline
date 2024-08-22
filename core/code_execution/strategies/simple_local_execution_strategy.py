from ..code_executor import CodeExecutionStrategy


class SimpleLocalCodeExecutor(CodeExecutionStrategy):
    def _execute(self, code_str: str):
        return exec(code_str)

