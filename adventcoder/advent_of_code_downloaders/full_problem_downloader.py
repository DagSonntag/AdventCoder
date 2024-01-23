from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

from pathlib import Path
import os

from adventcoder.file_path_templates import get_problem_answer_path, get_problem_input_text_path, get_problem_input_html_path, \
    get_problem_input_data_path


def download_advent_of_code_data(advent_of_code_website: str, year: int, data_folder_location: Path,
                                 github_username: [str] = None, github_password: [str] = None):
    """
    This script downloads all the problems and solutions from Advent of Code for a single year.
    It does this by:
    1. Opening a browser
    2. Logging into the website
    - For each day:
        - Download the part of the website that contains the relevant text
        - Split the text into the two parts
        - For each part, save the correct response and remove it from the original text
        - Save the text to a file (one for each day) in the data folder
        - Then also save the input data to the same folder
    - Close the browser

    Limitations:
    - Currently it uses the GitHub credentials (Google and twitter oath are also available) if provided, otherwise it
    will require manual login in the browser window. (difficult to automate more due to two-factor authentication)
    - Currently it assumes the problems have been solved in the past, or nothing is saved.
    - No error handling is done, so if something goes wrong, it will just crash.
    - No statistics are saved (e.g. how many people solved the problem, how long it took, etc.)
    """
    logging.info("Starting data download")
    save_folder_path = get_problem_input_text_path(Path(data_folder_location), year, 1, 1).parent
    save_folder_path.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    # start in full size
    options.add_argument("--start-maximized")
    # Note that we need to run in not headless mode to be able to log in using oauth (and two-factor authentication)

    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, 10)
    browser.get(advent_of_code_website + '/' + str(year) + '/auth/login')

    # Sign in using oauth from GitHub if credentials are provided, else let the user sign in manually
    if github_username is not None and github_password is not None:
        browser.find_element(By.LINK_TEXT, "[GitHub]").click()
        # type email
        wait.until(ec.presence_of_element_located((By.ID, "login_field"))).send_keys(github_username)
        # type password
        wait.until(ec.presence_of_element_located((By.ID, "password"))).send_keys(github_password)
        # click signin
        wait.until(ec.presence_of_element_located((By.NAME, "commit"))).click()
        # Here two-factor authentication is required and might have to be done manually.
    # Wait until we are back at advent of code
    logging.info("Waiting for manually finishing login")
    WebDriverWait(browser, 1000).until(ec.title_contains('Advent of Code'))
    logging.info("Login finished, continuing data download")

    # For each day:
    for day_nr in range(1, 26):
        # Download the part of the website that contains the relevant text
        browser.get(f'{advent_of_code_website}/{year}/day/{day_nr}')
        question_text = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "day-desc")))

        # Find the answers paragraphs with the text "Your puzzle answer was"
        question_ans_paragraphs = browser.find_elements(By.XPATH, "//p[contains(text(), 'Your puzzle answer was')]")
        # Find the <code> tag for each of these paragraphs and the text inside
        question_ans = [q.find_element(By.TAG_NAME, "code").text for q in question_ans_paragraphs]

        if len(question_ans) > len(question_text):
            raise ValueError(f'There are more answers ({len(question_ans)}) than questions '
                             f'({len(question_text)}) found for day {day_nr}')

        # Save the text to a file (one for each day) in the data folder
        for i, ans in enumerate(question_ans):
            logging.info(f"Saving day {day_nr} part {i + 1}")
            with open(get_problem_input_text_path(data_folder_location, year, day_nr, i+1), 'w') as f:
                f.write(question_text[i].text)
            with open(get_problem_input_html_path(data_folder_location, year, day_nr, i+1),'w') as f:
                f.write(question_text[i].get_attribute('innerHTML'))
            with open(get_problem_answer_path(data_folder_location, year, day_nr, i+1), 'w') as f:
                f.write(ans)

        # Then also save the input data
        browser.get(f'{advent_of_code_website}/{year}/day/{day_nr}/input')
        # Wait until the input data is loaded
        body_text = wait.until(ec.presence_of_element_located((By.TAG_NAME, "Body"))).text
        body_text += '\n'  # Add a newline at the end of the file
        # Save the input data
        with open(get_problem_input_data_path(data_folder_location, year, day_nr), 'w') as f:
            f.write(body_text)
    browser.close()
    print("Finished downloading data")


if __name__ == '__main__':
    # Add the main logger to print to the prompt
    logging.basicConfig(level=logging.INFO)
    # Get the user credentials to use from the environment variables
    download_advent_of_code_data(
        advent_of_code_website='https://adventofcode.com',
        year=2023,
        data_folder_location=Path('data'),
        github_username=os.environ.get('GITHUB_USERNAME') if 'GITHUB_USERNAME' in os.environ else None,
        github_password=os.environ.get('GITHUB_PASSWORD') if 'GITHUB_PASSWORD' in os.environ else None)
