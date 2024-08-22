from abc import ABC, abstractmethod


class CodeExecutionStrategy(ABC):
    def execute_code(self, code_str: str) -> object:
        preprocessed_code = self._preprocess_code_input(code_str)
        execution_output = self._execute(preprocessed_code)
        return self._postprocess_response(execution_output)

    @abstractmethod
    def _execute(self, code_str: str):
        pass

    def _preprocess_code_input(self, input_obj: str) -> str:
        return input_obj

    def _postprocess_response(self, output_obj: object) -> object:
        return output_obj
