import pytest

from core.code_execution.strategies.simple_local_execution_strategy import SimpleLocalCodeExecutor


@pytest.fixture
def executor():
    return SimpleLocalCodeExecutor()


@pytest.mark.parametrize(
    "code_str, input_value, expected_result, expected_stdout",
    [
        (
                """
            def main(input):
                return input * 2
            """,
                5,
                10,
                "",
        ),
    ],
)
def test_successful_execution(executor: SimpleLocalCodeExecutor,
                              code_str,
                              input_value,
                              expected_result,
                              expected_stdout):
    result, stdout = executor.execute_code(code_str, input_value)

    assert result == expected_result
    assert stdout == expected_stdout
