import os
import subprocess


def create_requirements_txt(save_path: str, python_interpreter: str) -> None:
    """
    Generate a requirements.txt file from the specified Python interpreter.

    :param save_path: Path to save the requirements.txt file.
    :param python_interpreter: Path to the Python interpreter to use.
    """
    if not os.path.exists(python_interpreter):
        print(f"Error: Python interpreter '{python_interpreter}' not found.")
        return

    try:
        result = subprocess.run(
            [python_interpreter, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True,
        )
        requirements = result.stdout.strip()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(requirements)

        print(f"requirements.txt created successfully at: {save_path}")

    except subprocess.CalledProcessError as error:
        print(f"Error running pip freeze: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    SAVE_PATH = "requirements.txt"
    PYTHON_INTERPRETER = r"C:\Users\libin\01_Project\Automation_Projects\.venv\Scripts\python.exe"  # Change this path to interpreter path
    create_requirements_txt(SAVE_PATH, PYTHON_INTERPRETER)
