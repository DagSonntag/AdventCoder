import os
import subprocess
from adventcoder.constants.evaluation_constants import GENERATED_CODE_EXECUTION_TIMEOUT


def execute_code(python_code: str, input_data_str: str) -> str:
    """
    Executes the code and returns the output as a string with a call to the aoc function provided (having the
    input_data_str as input). In case of an error it raises an appropriate exception.

    Note: This function is not secure and should not be used for code that can be malicious nor on platforms with
    sensitive information since it will execute with the same privileges and environment as the current environment.
    """

    # Encode the input data string into bytes
    input_data_bytes = input_data_str.encode('utf-8')

    # Add in read the input data file
    code_to_execute = python_code
    code_to_execute += f"\ninput_data = {repr(input_data_bytes)}\n"
    # Add in the call to the function
    code_to_execute += f"\nprint(aoc(input_data.decode('utf-8')))"

    # Execute the code and capture the output
    try:
        completed_process = subprocess.run(['python', '-c', code_to_execute], capture_output=True,
                                           text=True, timeout=GENERATED_CODE_EXECUTION_TIMEOUT, env=os.environ)
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"The code took more than {GENERATED_CODE_EXECUTION_TIMEOUT} seconds to execute")
    if completed_process.returncode != 0:
        raise RuntimeError(completed_process.stderr.split('\n')[-2])
    else:
        return completed_process.stdout.split('\n')[-2]
