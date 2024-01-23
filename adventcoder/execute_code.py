import os
import subprocess


def execute_code(python_code: str, input_data_str: str) -> str:
    """
    Executes the code and returns the output as a string with a call to the aoc function provided (having the
    input_data_str as input). In case of an error it raises an appropriate exception.
    :param python_code:
    :param input_data_str:
    :return:
    """

    # Encode the input data string into bytes
    input_data_bytes = input_data_str.encode('utf-8')

    # Add in read the input data file
    code_to_execute = python_code
    code_to_execute += f"\ninput_data = {repr(input_data_bytes)}\n"
    # Add in the call to the function
    code_to_execute += f"\nprint(aoc(input_data.decode('utf-8')))"

    # Execute the code and capture the output
    timeout = 60
    try:
        completed_process = subprocess.run(['python', '-c', code_to_execute], capture_output=True,
                                           text=True, timeout=timeout, env=os.environ)
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"The code took more than {timeout} seconds to execute")
    if completed_process.returncode != 0:
        raise RuntimeError(completed_process.stderr.split('\n')[-2])
    else:
        return completed_process.stdout.split('\n')[-2]
