import requests
import pandas as pd

# 🔑 Replace with your Clockify API Key
API_KEY = "YOUR_API_KEY"
WORKSPACE_ID = "YOUR_WORKSPACE_ID"  # Get it from Clockify API using get_workspace_id.sh

# 🗂️ Read time entries from CSV
df = pd.read_csv("timesheet.csv")

# 🔍 Get user ID from Clockify
def get_user_id():
    headers = {"X-Api-Key": API_KEY}
    response = requests.get("https://api.clockify.me/api/v1/user", headers=headers)
    response.raise_for_status()
    return response.json()["id"]


USER_ID = get_user_id()


# 🎯 Function to create time entry
def create_time_entry(start_time, end_time, project_name, task_name, description):
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    # Convert times to Clockify format
    start_iso = f"{start_time}:00Z"
    end_iso = f"{end_time}:00Z"

    # 🔄 Get project ID dynamically (if needed)
    project_id = get_project_id(project_name)
    if task_name.lower() != "skip":
        task_id = get_task_id(project_id, task_name)
    else:
        task_id = ''

    data = {
        "start": start_iso,
        "end": end_iso,
        "billable": False,
        "description": description,
        "projectId": project_id,
        "taskId": task_id,
        "userId": USER_ID
    }

    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/time-entries"
    response = requests.post(url, headers=headers, json=data)
    print(response.json())


def get_task_id(PROJECT_ID, TASK_NAME):
    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/tasks"
    headers = {"X-Api-Key": API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    tasks = response.json()
    for task in tasks:
        if task["name"].lower() == TASK_NAME.lower():
            return task["id"]

    raise ValueError(f"Task '{TASK_NAME}' not found in project!")

# 🔍 Get project ID from name
def get_project_id(project_name):
    projects = []
    for n in range(1, 3):
        url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects?page={n}&page-size={100}"
        headers = {"X-Api-Key": API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects += response.json()

    for project in projects:
        if project["name"].lower() == project_name.lower():
            return project["id"]
    raise ValueError(f"Project '{project_name}' not found!")


# 🔄 Process each row from CSV
for _, row in df.iterrows():
    date = row["date"]
    start_time = f"{date}T{row['start_time']}"
    end_time = f"{date}T{row['end_time']}"
    project = row["project"]
    task = row["task"]
    description = row["description"]

    create_time_entry(start_time, end_time, project, task, description)
#
print("All time entries uploaded successfully!")
