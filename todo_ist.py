import requests
import json
import os
import configparser

# Load configuration from Settings folder
CONFIG_DIR = "Settings"
CONFIG_FILE = os.path.join(CONFIG_DIR, "toddoist_config.ini")

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
TODOIST_API_TOKEN = config.get("TODOIST", "API_TOKEN")

# Constants
API_URL = "https://api.todoist.com/rest/v2/tasks"
PROJECTS_URL = "https://api.todoist.com/rest/v2/projects"
OUTPUT_DIR = "output/todoist"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "tasks.json")

class TodoistTaskManager:
    """Handles fetching, saving, and creating tasks with exception handling."""
    def __init__(self, api_token, api_url, output_dir, output_file):
        self.api_token = api_token
        self.api_url = api_url
        self.output_dir = output_dir
        self.output_file = output_file

    def fetch_tasks(self):
        """Fetch tasks from Todoist API."""
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(self.api_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tasks: {e}")
            return []

    def save_tasks(self, tasks):
        """Save tasks to a JSON file."""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4)
            print(f"Tasks saved to {self.output_file}")
        except (OSError, IOError) as e:
            print(f"Error saving tasks: {e}")

    def create_task(self, content, description=None, parent_id=None):
        """Create a task in Todoist."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            data = {"content": content}
            if description:
                data["description"] = description
            if parent_id:
                data["parent_id"] = parent_id
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating task: {e}")
            return None

    def create_main_task_with_subtasks(self, main_task_name, main_task_description, subtask_data):
        """Create a main task with subtasks in Todoist."""
        main_task = self.create_task(main_task_name, main_task_description)
        if main_task:
            main_task_id = main_task.get("id")
            for index, (title, description) in enumerate(subtask_data.items(), start=1):
                self.create_task(f"{index}. {title}", description, parent_id=main_task_id)

    def process_tasks(self):
        """Fetch and save tasks."""
        tasks = self.fetch_tasks()
        self.save_tasks(tasks)
        print(json.dumps(tasks, indent=4))

if __name__ == "__main__":
    manager = TodoistTaskManager(TODOIST_API_TOKEN, API_URL, OUTPUT_DIR, OUTPUT_FILE)
    manager.process_tasks()
    
    # Example usage for generic task creation
    task_data = {
        "January": "Tasks for January",
        "February": "Tasks for February"
    }
    manager.create_main_task_with_subtasks("Yearly Tasks", "Overview of tasks for the year", task_data)
