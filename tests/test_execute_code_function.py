import pytest
from adventcoder.execute_code import execute_code


def test_execute_code_success():
    python_code = """
def aoc(input_data):
    return input_data
"""
    input_data_str = "test input"
    expected_output = "test input"  # The output will have a trailing newline
    assert execute_code(python_code, input_data_str) == expected_output


def test_execute_code_error():
    python_code = """
def aoc(input_data):
    raise ValueError("test error")
"""
    input_data_str = "test input"
    with pytest.raises(RuntimeError) as excinfo:
        execute_code(python_code, input_data_str)
    assert "test error" in str(excinfo.value)


def test_execute_code_newline_in_input():
    python_code = """
def aoc(input_data):
    return input_data
"""
    input_data_str = "test\ninput"
    expected_output = "input"
    output = execute_code(python_code, input_data_str)
    assert output == expected_output, f"Expected '{expected_output}', but got '{output}'"


def test_execute_code_environment():
    python_code = """
import pandas as pd
import numpy as np
def aoc(input_data):
    return input_data
"""
    input_data_str = "test_input"
    expected_output = "test_input"
    output = execute_code(python_code, input_data_str)
    assert output == expected_output, f"Expected '{expected_output}', but got '{output}'"


@pytest.mark.skip(reason="This test takes 60 seconds to run")
def test_execute_code_infinite_loop():
    python_code = """
def aoc(input_data):
    while True:
        pass
"""
    input_data_str = "test input"
    with pytest.raises(TimeoutError):
        execute_code(python_code, input_data_str)