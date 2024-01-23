import logging
from adventcoder.models.vertex_ai_model import VertexAiModel
from adventcoder.file_path_templates import *
from adventcoder.execute_code import execute_code


def evaluate_model_instance(model_instance: VertexAiModel, data_path: Path, year: int, day_range: range = range(1, 26),
                            part_range: range = range(1, 3)):
    """
    Evaluates the model on all the problems in a given year by loading the problem data, running the model,
    and returning the result as a list of dicts including all relevant info.
    """
    results = list()
    for day_nr in day_range:
        for part_nr in part_range:
            problem_html_path = get_problem_input_html_path(data_path, year, day_nr, part_nr)
            problem_data_path = get_problem_input_data_path(data_path, year, day_nr)
            correct_ans_path = get_problem_answer_path(data_path, year, day_nr, part_nr)

            if problem_html_path.exists() and problem_data_path.exists() and correct_ans_path.exists():
                # Get the data
                problem_html_str = problem_html_path.read_text()
                problem_data_str = problem_data_path.read_text()
                correct_ans_str = correct_ans_path.read_text()
                # Make the model instance generate the code
                generated_code = model_instance.generate_code(problem_html_str, problem_data_str)
                # Execute the code
                try:
                    predicted_ans = execute_code(generated_code, problem_data_str)
                except RuntimeError as e:
                    predicted_ans = e.__repr__()
                except TimeoutError:
                    predicted_ans = "Timeout"
                # Save output for comparison
                results.append({
                    "year": year,
                    "day": day_nr,
                    "part": part_nr,
                    "problem_html": problem_html_str,
                    "correct_ans": correct_ans_str,
                    "predicted_ans": predicted_ans,
                    "generated_code": generated_code,
                    "problem_data_str": problem_data_str
                })
                logging.info(f"Year {year}, day {day_nr}, part {part_nr}: {correct_ans_str} vs {predicted_ans}")
    return results
