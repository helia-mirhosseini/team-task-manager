import requests
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox


class UserWindow(QWidget):
    def __init__(self, api_url, username):
        super().__init__()
        self.api_url = api_url  # Base URL for the FastAPI backend
        self.username = username  # Username of the logged-in user

        self.setWindowTitle(f"Dashboard {username}")  # UI Title
        self.resize(500, 400)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Ariel', sans-serif; /* Replace with your Persian font */
                font-size: 14px;
                background-color: #f4f4f8;
            }
            QLabel {
                color: #333;
                text-align: right;
            }
            QPushButton {
                background-color: #07c5c2;
                border: 1px solid #07c5c2;
                border-radius: 8px;
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #029e9f;
                border: 1px solid #029e9f;
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #078385, stop: 1 #0b6264
                );
                border: 1px solid #0e5253;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Label
        header_label = QLabel("Your Tasks")  # Adjusted label text
        layout.addWidget(header_label)

        # Task List
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Buttons
        refresh_button = QPushButton("Refresh Tasks")
        refresh_button.clicked.connect(self.load_tasks)  # Connect to the method to load tasks
        layout.addWidget(refresh_button)

        complete_button = QPushButton("Mark as Complete")
        complete_button.clicked.connect(self.mark_task_complete)  # Connect to the method to mark tasks
        layout.addWidget(complete_button)

        self.setLayout(layout)

        # Load tasks initially
        self.load_tasks()

    def load_tasks(self):
        """Fetch tasks from the backend and display them in the task list."""
        try:
            response = requests.get(f"{self.api_url}/tasks/{self.username}/")
            if response.status_code == 200:
                tasks = response.json().get("task", [])
                self.task_list.clear()  # Clear the list before adding new tasks
                for task in tasks:
                    # Display tasks as "<title>: <description> (Status: <status>)"
                    self.task_list.addItem(f"{task['title']}: {task['description']} (Status: {task['status']})")
                    task['task_id'] = task['task_id']  # Include task IDs for status updates
            else:
                QMessageBox.critical(self, "Error", f"Failed to load tasks: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def mark_task_complete(self):
        """Mark the selected task as complete by calling the backend."""
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark as complete.")
            return

        selected_item = selected_items[0].text()
        # Extract task title (assuming it's before the first colon ":")
        task_title = selected_item.split(":")[0].strip()

        try:
            # Call the backend to get task_id (provided by backend improvements)
            response = requests.get(f"{self.api_url}/tasks/{self.username}/")
            if response.status_code == 200:
                tasks = response.json().get("task", [])
                task_id = None
                for task in tasks:
                    if task["title"] == task_title:
                        task_id = task.get("task_id")  # Ensure the backend provides task_id
                        break

                if task_id:
                    # Mark the task as complete
                    update_response = requests.put(f"{self.api_url}/tasks/{task_id}/status", params={"new_status": "Completed"})
                    if update_response.status_code == 200:
                        QMessageBox.information(self, "Success", "Task marked as complete!")
                        self.load_tasks()  # Refresh the task list
                    else:
                        QMessageBox.critical(self, "Error", f"Failed to update task: {update_response.json().get('detail', 'Unknown error')}")
                else:
                    QMessageBox.critical(self, "Error", "Task ID not found. Please try again.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch tasks: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
