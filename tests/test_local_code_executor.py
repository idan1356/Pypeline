import pytest
from typing import Any

from core.code_execution.strategies.simple_local_execution_strategy import PythonLocalCodeExecutor
from tests.conftest import (simple_working_code,
                            no_main_func_gateway_code1,
                            no_main_func_gateway_code2,
                            main_not_callable,
                            code_runtime_error,
                            code_syntax_error1,
                            code_syntax_error2,
                            code_syntax_error3)


@pytest.fixture
def executor():
    return PythonLocalCodeExecutor()


@pytest.mark.parametrize("code_str, input_value, expected_result",
                         [(simple_working_code, 5, 10), (simple_working_code, "test", "testtest")])
def test_successful_execution(executor: PythonLocalCodeExecutor,
                              code_str: str,
                              input_value: Any,
                              expected_result: Any):
    result, _stdout = executor.execute_code(code_str, input_value)
    assert result == expected_result


@pytest.mark.parametrize("code_str, input_value, expected_stdout", [(simple_working_code, 5, "5\n"),
                                                                    (simple_working_code, 10, "10\n"),
                                                                    (simple_working_code, "test", "test\n")])
def test_capture_stdout(executor: PythonLocalCodeExecutor,
                        code_str: str,
                        input_value: Any,
                        expected_stdout: str):
    _, stdout = executor.execute_code(code_str, input_value)
    assert stdout == expected_stdout


@pytest.mark.parametrize("code_str",
                         [no_main_func_gateway_code1, no_main_func_gateway_code2])
def test_no_main_gateway_exception(executor: PythonLocalCodeExecutor, code_str: str):
    with pytest.raises(KeyError):
        executor.execute_code(code_str, "input_not_relevant")


@pytest.mark.parametrize("code_str", [main_not_callable])
def test_main_is_not_callable(executor: PythonLocalCodeExecutor, code_str: str):
    with pytest.raises(TypeError):
        executor.execute_code(code_str, "input_not_relevant")


@pytest.mark.parametrize("code_str", [code_runtime_error])
def test_code_runtime_error(executor: PythonLocalCodeExecutor, code_str: str):
    with pytest.raises(RuntimeError):
        executor.execute_code(code_str, "input_not_relevant")


@pytest.mark.parametrize("code_str", [code_syntax_error1, code_syntax_error2, code_syntax_error3])
def test_code_syntax_error(executor: PythonLocalCodeExecutor, code_str: str):
    with pytest.raises(ValueError):
        executor.execute_code(code_str, "input_not_relevant")
