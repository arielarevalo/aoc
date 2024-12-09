import os
import requests
import nbformat
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup

# Load session cookie from .env file
load_dotenv()
SESSION_COOKIE = os.getenv("AOC_SESSION_COOKIE")
if not SESSION_COOKIE:
    raise ValueError("Advent of Code session cookie is required. Set it in a .env file as AOC_SESSION_COOKIE.")

# Get the current year and day dynamically
CURRENT_YEAR = datetime.now().year
CURRENT_DAY = datetime.now().day

# Constants
BASE_URL = f"https://adventofcode.com/{CURRENT_YEAR}/day"
ROOT_DIR = f"./{CURRENT_YEAR}"
HEADERS = {"Cookie": f"session={SESSION_COOKIE}"}


def ensure_directory(path):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path)


def fetch_input(day):
    """Fetch the input data for the given day."""
    response = requests.get(f"{BASE_URL}/{day}/input", headers=HEADERS)
    response.raise_for_status()
    return response.text.strip()


def create_jupyter_notebook(day):
    """Create a Jupyter notebook that displays a link to the puzzle and reads the input."""
    notebook_path = os.path.join(ROOT_DIR, str(day), "answer.ipynb")

    nb = nbformat.v4.new_notebook()

    title = f"# Advent of Code {CURRENT_YEAR}, Day {day}"
    nb.cells.append(nbformat.v4.new_markdown_cell(title))

    code = "with open('input.txt', 'r') as f:\n    puzzle_input = f.read().strip()"
    nb.cells.append(nbformat.v4.new_code_cell(code))

    first_link = f"## [First Puzzle:]({BASE_URL}/{day})"
    nb.cells.append(nbformat.v4.new_markdown_cell(first_link))
    nb.cells.append(nbformat.v4.new_code_cell())

    second_link = f"## [Second Puzzle:]({BASE_URL}/{day}/#part2)"
    nb.cells.append(nbformat.v4.new_markdown_cell(second_link))
    nb.cells.append(nbformat.v4.new_code_cell())

    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


def main():
    # Only fetch up to today's date, or day 25 whichever is smaller
    for day in range(1, min(26, CURRENT_DAY + 1)):
        day_dir = os.path.join(ROOT_DIR, str(day))
        input_file = os.path.join(day_dir, "input.txt")

        # Ensure directories exist
        ensure_directory(ROOT_DIR)
        ensure_directory(day_dir)

        # Get input if not already fetched
        if not os.path.exists(input_file):
            try:
                print(f"Fetching input for Day {day}...")
                input_data = fetch_input(day)
                with open(input_file, "w") as f:
                    f.write(input_data)
            except requests.HTTPError as e:
                print(f"Day {day}: Unable to fetch input. Error: {e}")
                continue

        # Create Jupyter notebook if not existing
        notebook_path = os.path.join(day_dir, "answer.ipynb")
        if not os.path.exists(notebook_path):
            print(f"Building notebook for Day {day}...")
            create_jupyter_notebook(day)


if __name__ == "__main__":
    main()
