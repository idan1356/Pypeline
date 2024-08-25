from contextlib import redirect_stdout
from io import StringIO
from types import CodeType
from typing import Callable, Dict, Any

from ..code_executor import CodeExecutionStrategy


class SimpleLocalCodeExecutor(CodeExecutionStrategy):
    PROGRAM_ENTRY_POINT: str = 'main'
    COMPILE_MODE: str = 'exec'
    FILE_NAME_PLACEHOLDER: str = 'str'

    # TODO: handle exceptions inside the class
    def _execute(self, code_str: str, input: Any) -> Any:
        """
        Compiles and execute the provided code string with the given input.

        :param code_str: The python code to be executed. (must have 'main' entrypoint)
        :param input: The input to be passed to the 'main' function.
        :return: # TODO: specify return
        """
        exec_namespace = {}

        code = self._compile_code(code_str)
        exec(code, exec_namespace)
        self._validate_namespace(exec_namespace)

        stdout = StringIO()
        with redirect_stdout(stdout):
            res = self._run_main_function(exec_namespace[self.PROGRAM_ENTRY_POINT], input)

        return res, stdout.getvalue()

    def _compile_code(self, code_str: str) -> CodeType:
        try:
            compiled_code = compile(code_str, self.FILE_NAME_PLACEHOLDER, self.COMPILE_MODE)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in the provided code: {e}")
        return compiled_code

    def _validate_namespace(self, exec_namespace: Dict[str, Any]) -> None:
        """
        Validates that the namespace contains core callable 'main' function.

        :param exec_namespace: dictionary of python AST objects of compiled python code
        :return: None
        """
        if 'main' not in exec_namespace:
            raise KeyError("The code must define core 'main' function.")
        if not callable(exec_namespace[self.PROGRAM_ENTRY_POINT]):
            raise TypeError("'main' in the code is not callable.")

    def _run_main_function(self, main_func: Callable[[Any], Any], input: Any) -> Any:
        try:
            res = main_func(input)
        except Exception as e:
            raise RuntimeError(f"Error during 'main' function execution: {e}")
        return res
