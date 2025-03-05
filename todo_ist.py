import os
import json
import requests
import configparser
from tqdm import tqdm
# Load configuration from Settings folder
CONFIG_DIR = "Settings"
CONFIG_FILE = os.path.join(CONFIG_DIR, "todoist_config.ini")

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
TODOIST_API_TOKEN = config.get("TODOIST", "API_TOKEN", fallback=None)

if TODOIST_API_TOKEN is None:
    raise ValueError("API Token not found in configuration file.")

class TodoistTaskManager:
    """
    A manager class to handle fetching and saving tasks from Todoist API using SOLID principles.
    """
    API_URL = "https://api.todoist.com/rest/v2/tasks"
    OUTPUT_DIR = "output/todoist"
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, "tasks.json")

    def __init__(self, api_token):
        self.api_token = api_token

    def fetch_todoist_tasks(self):
        """Fetch tasks from Todoist API."""
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(self.API_URL, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tasks: {e}")
            return []

    def save_tasks_to_file(self, tasks):
        """Save tasks to a JSON file."""
        try:
            os.makedirs(self.OUTPUT_DIR, exist_ok=True)
            with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4)
            print(f"Tasks saved to {self.OUTPUT_FILE}")
        except (OSError, IOError) as e:
            print(f"Error saving tasks to file: {e}")

    def create_task(self, task_name, task_description, parent_id=None):
        """Create a task in Todoist."""
        try:
            headers = {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"}
            data = {"content": task_name, "description": task_description}
            if parent_id:
                data["parent_id"] = parent_id
            response = requests.post(self.API_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating task: {e}")
            return None

    def create_main_task_with_subtasks(self, main_task_name, main_task_description, subtask_data):
        """Create a main task with subtasks in Todoist."""
        try:
            main_task = self.create_task(main_task_name, main_task_description)
            if main_task:
                main_task_id = main_task.get("id")
                with tqdm(
                    total=len(subtask_data.items()),
                    desc="Adding Sub Tasks", 
                    bar_format="{l_bar}{bar:20} {n_fmt}/{total_fmt} [elapsed: {elapsed} | remaining: {remaining} | avg: {rate_fmt}] {postfix}",
                    dynamic_ncols=True
                ) as progress_bar:
                    for index, (title, description) in enumerate(subtask_data.items(), start=1):
                        try:
                            self.create_task(f"{index}. {title}", description, parent_id=main_task_id)
                            task_name = f"Task {index}. {title}"
                            progress_bar.set_postfix({"Added": task_name})
                        finally:
                            progress_bar.update(1)
        except Exception as e:
            print(f"Error creating main task with subtasks: {e}")

    def download_tasks(self):
        """Fetch and save tasks."""
        try:
            tasks = self.fetch_todoist_tasks()
            self.save_tasks_to_file(tasks)
            print(json.dumps(tasks, indent=4))  # Pretty print tasks
        except Exception as e:
            print(f"Error in downloading tasks: {e}")

if __name__ == "__main__":
    from date_todo_ist import generate_sub_task
    main_task_name = "Copy Folder Itmes"
    main_task_description = "Copy Folder Itmes"
    sub_task = generate_sub_task("2024-01","2025-01")
    manager = TodoistTaskManager(TODOIST_API_TOKEN)

    action = "create_task"  # Change this to "create_task" for task creation

    if action == "download_tasks":
        try:
            manager.download_tasks()
        except Exception as e:
            print(f"Unexpected error: {e}")
    elif action == "create_task":
        try:
            manager.create_main_task_with_subtasks(main_task_name, main_task_description, sub_task)
        except Exception as e:
            print(f"Error creating tasks: {e}")
