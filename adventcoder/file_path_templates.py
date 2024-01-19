from pathlib import Path

PROBLEM_INPUT_TEXT = "day_{day_nr}_part_{part_nr}_text.txt"
PROBLEM_INPUT_HTML = "day_{day_nr}_part_{part_nr}.html"
PROBLEM_ANSWER = "day_{day_nr}_part_{part_nr}_ans.txt"
PROBLEM_INPUT_DATA = "day_{day_nr}_input_data.txt"


def get_problem_input_text_path(save_folder_path: Path, year: int, day_nr: int, part_nr: int) -> Path:
    return save_folder_path / str(year) / PROBLEM_INPUT_TEXT.format(day_nr=day_nr, part_nr=part_nr)


def get_problem_input_html_path(save_folder_path: Path, year: int, day_nr: int, part_nr: int) -> Path:
    return save_folder_path / str(year) / PROBLEM_INPUT_HTML.format(day_nr=day_nr, part_nr=part_nr)


def get_problem_answer_path(save_folder_path: Path, year: int, day_nr: int, part_nr: int) -> Path:
    return save_folder_path / str(year) / PROBLEM_ANSWER.format(day_nr=day_nr, part_nr=part_nr)


def get_problem_input_data_path(save_folder_path: Path, year: int, day_nr: int) -> Path:
    return save_folder_path / str(year) / PROBLEM_INPUT_DATA.format(day_nr=day_nr)



