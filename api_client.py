import requests
from PyQt6.QtWidgets import QMessageBox
import bcrypt

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def login(self, username, password):
        """Check user credentials and return role if valid."""
        response = requests.get(f"{self.base_url}/users/", params={"username": username, "password": password})
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"API response: {user_data}")  # Debugging to see the role returned
            
            # No need to compare passwords on the frontend, as the backend already handled this
            if "role" in user_data:
                return user_data["role"]  # Return the role only if the backend successfully authenticated
            else:
                print("Role not found in the response.")
                return None  # If role is not found, return None (authentication failed)
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None  # User not found or other error
        

    def user_with_tasks(self):
        """Fetch all users with tasks."""
        url = f"{self.base_url}/users/tasks/"
        print(f"Fetching data from {url}")  # Debugging
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Response JSON:", data)  # Debugging line

            users_list = data.get("users with tasks", [])
            
            if not isinstance(users_list, list):
                print("Unexpected data format:", users_list)
                return []
            
            return [user.get("username", "Unknown") if isinstance(user, dict) else user for user in users_list]

        print(f"Failed to fetch data. Status Code: {response.status_code}, Response: {response.text}")
        return []



    def assign_task(self, username, title, description):
        """Assign a task to a user."""
        data = {"title": title, "description": description}
        response = requests.post(f"{self.base_url}/tasks/?username={username}", json=data)
        return response.status_code == 200

    def get_user_tasks(self, username):
        """Fetch tasks assigned to a user."""
        response = requests.get(f"{self.base_url}/tasks/{username}/")
        if response.status_code == 200:
            return response.json().get("task", [])
        return []

    def update_task_status(self, task_id, new_status):
        """Update the status of a task."""
        response = requests.put(f"{self.base_url}/tasks/{task_id}/status", params={"new_status": new_status})
        return response.status_code == 200

    def update_user_role(self, user, new_role):
        """Update the role of a user."""
        response = requests.put(f"{self.base_url}/users/{user}/role", json={"role": new_role})
        return response.status_code == 200

    def delete_user(self, user):
        """Delete a user."""
        response = requests.delete(f"{self.base_url}/users/{user}/")
        return response.status_code == 200

    def delete_task(self, task_title):
        """Delete a task."""
        response = requests.delete(f"{self.base_url}/tasks/{task_title}/")
        return response.status_code == 200
    
    def insert_user(self,username, password, role):
        """Function to insert a new user via the FastAPI backend"""
        
        url = f"{self.base_url}/users/"
        data = {
            "username": username,
            "password": password,
            "role": role
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)  # Use `json=` instead of `params=`

        if response.status_code == 200:
            return response.json()
        else:
            QMessageBox.critical(None, "Error", f"Failed to add user {username}. Error: {response.text}")
    
    
    def search_task(self, username, title):
        """
        Function to get tasks assigned to a specific user via the FastAPI backend.
        Optionally, if a task title is provided, it will be used to search tasks by name (partial match).
        """
        url = f"{self.base_url}/tasks/"
        
        # If a task title is given, include it as a query parameter:
        params = {key: value for key, value in [("title", title), ("username", username)] if value}

        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            tasks = response.json()
            print(f"Tasks for {username}:")
            for task in tasks["task"]:
                print(f" - {task['title']}: {task['description']} (Status: {task['status']})")
            return tasks
        else:
            print(f"Failed to retrieve tasks for {username}. Error: {response.text}")
            return None