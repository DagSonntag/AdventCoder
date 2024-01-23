from langchain_google_vertexai import VertexAI

import logging


class VertexAiModel:
    """ A default model from vertex ai. (non-fine-tuned) """
    # "CodeLlama-7b-hf"
    # code-bison@002
    def __init__(self, model_name: str = "CodeLlama-7b"):
        """
        Initializes the model with the environment set authentication details
        :param model_name:
        """
        self.llm = VertexAI(model=model_name, max_output_tokens=2048, max_input_tokens=4000)

    @staticmethod
    def generate_query(problem_text: str, problem_data_str: str) -> str:
        """
        Generates the query for the model to solve the problem where the function takes the problem_data_text as input
        and returns the answer as a string.
        :param problem_text:
        :param problem_data_str:
        :return:
        """
        pre_text = (
            'Write a python function that solves the problem described in the problem section for the data in the '
            'data section.\n'
            'The answer should be on the form: \n'
            '\n'
            'def aoc(input_str:str) -> str:\n'
            '   # solve_problem here\n'
            '   return final_result\n'
            '\n\n')
        delimiter = "=" * 100 + "\n"
        simplified_problem_data = "\n".join(problem_data_str.split("\n")[0:10]) + "\n"

        query_prompt_string = f'{pre_text}{delimiter}{problem_text}\n{delimiter}input_str="{simplified_problem_data}"\n'
        return query_prompt_string

    def generate_code(self, problem_text: str, problem_data_str: str) -> str:
        """
        Generates the python code for a function and function_call that solves the problem where the function takes the
        problem_data_text as input and returns the answer as a string.
        :param problem_text:
        :param problem_data_str:
        :return:
        """
        query_prompt_string = self.generate_query(problem_text, problem_data_str)
        logging.debug(query_prompt_string)
        generated_code = self.llm.invoke(query_prompt_string)

        # Remove the markdown part from the code:
        if generated_code.startswith(' ```python\n'):
            generated_code = generated_code[11:]
        if generated_code.endswith('```'):
            generated_code = generated_code[:-3]
        logging.debug(generated_code)

        return generated_code
