# admin_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QTextEdit, QPushButton, QMessageBox, QToolBar,QGroupBox,QListWidget
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from api_client import APIClient
from database import Database

class SidebarTab(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text: str, base_icon_path: str, arrow_icon_path: str, parent=None, icon_bg_color: str = None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        self.setLayout(layout)

        # Base icon with an optional circular background.
        self.icon_label = QLabel()
        if icon_bg_color:
            # Apply a circular background using the provided color.
            self.icon_label.setStyleSheet(f"""
                background-color: {icon_bg_color};
                border-radius: 15px;
                padding: 3px;
            """)
             # Set a fixed size to preserve the circular shape
            self.icon_label.setFixedSize(30, 30)
            # Set the icon pixmap (20x20) and center it.
            self.icon_label.setPixmap(QIcon(base_icon_path).pixmap(20, 20))
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.icon_label.setPixmap(QIcon(base_icon_path).pixmap(20, 20))
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)

        # Tab title.
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(text_label)

        layout.addStretch()

        # Arrow icon.
        arrow_label = QLabel()
        arrow_label.setPixmap(QIcon(arrow_icon_path).pixmap(12, 12))
        layout.addWidget(arrow_label)

        # Styling for hover effect.
        self.setStyleSheet("""
            SidebarTab {
                background-color: transparent;
            }
            SidebarTab:hover {
                background-color: #e0e0e0;
            }
        """)

    def mousePressEvent(self, event):
        self.clicked.emit()

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = APIClient()  # Uses the API client instance
        self.db = Database()
        self.setWindowTitle("Admin Dashboard")
        self.resize(500, 500)

        # Global style sheet for a modern, clean look.
        self.setStyleSheet("""
            QComboBox {
                background-color: #fff; /* White background for high contrast */
                color: #000;           /* Black text for readability */
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #fff; /* Ensures dropdown menu items have white background */
                color: #000;           /* Ensures text within dropdown is black */
                selection-background-color: #4997e8; /* Highlight color for selected item */
                selection-color: white; /* White text for the selected item */
            }
            QWidget {
                background-color: #f4f4f8;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;   /* Neutral background for text fields */
                color: black;              /* High contrast text color */
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 5px;
                background-color: #f0f0f0; /* A slightly darker light gray */
                color: #333;
                font-size: 14px;
            }

            QListWidget::item {
                background-color: #e0e0e0; /* A bit darker for each item */
                margin: 3px;
                padding: 8px;
                border-radius: 4px;
            }

            QListWidget::item:selected {
                background-color: #347cdc;  /* A strong blue when selected */
                color: white;
            }
            QPushButton {
                background-color: #4997e8;
                border: 1px solid #4997e8;
                border-radius: 8px;
                color: white;
                padding: 8px;
                font-size: 14px;
                font-weight: bold
            }
            QPushButton:hover {
                background-color: #347cdc;
                border: 1px solid #347cdc;
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #347cdc, stop: 1 #2961be
                );
                border: 1px solid #2954a4;
            }
        """)

        # --- Setup Movable Sidebar Toolbar ---
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setOrientation(Qt.Orientation.Vertical)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.setMovable(True)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        # Create custom sidebar tabs.
        # For the "Assign Task" tab, add a circular background (color: #c4e2f9)
        self.assign_tab = SidebarTab(
            "Assign Task", "assign_icon.png", "arrow_icon.png", self, icon_bg_color="#c4e2f9"
        )
        self.roles_tab = SidebarTab(
            "Manage Users", "roles_icon.png", "arrow_icon.png", self, icon_bg_color="#c4e2f9"
        )
        self.task_tab = SidebarTab(
            "Manage Tasks", "manage_task_icon.png", "arrow_icon.png", self, icon_bg_color="#c4e2f9"
        )

        self.toolbar.addWidget(self.assign_tab)
        self.toolbar.addWidget(self.roles_tab)
        self.toolbar.addWidget(self.task_tab)

        self.assign_tab.clicked.connect(self.show_assign_panel)
        self.roles_tab.clicked.connect(self.show_users_panel)
        self.task_tab.clicked.connect(self.show_manage_task_panel)
        
        # --- Create the Central Widget and Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        central_widget.setLayout(self.main_layout)

        # --- Panel for "Assign Task" ---
        self.assign_panel = QWidget()
        assign_layout = QVBoxLayout()
        assign_layout.setContentsMargins(0, 0, 0, 0)
        assign_layout.setSpacing(10)
        self.assign_panel.setLayout(assign_layout)
        
        assign_header_label = QLabel("Assign Task To User")
        assign_header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d2d2d;")
        assign_layout.addWidget(assign_header_label)
        
        # User selection.
        user_layout = QHBoxLayout()
        user_label = QLabel("Select User:")
        user_label.setStyleSheet("font-size: 14px;")
        self.user_combo = QComboBox()
        self.user_combo.setStyleSheet("QComboBox { padding: 4px; }")
        users = self.api.user_with_tasks()
        self.user_combo.addItems(users)
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_combo)
        assign_layout.addLayout(user_layout)
        
        # Task Title Input.
        title_layout = QHBoxLayout()
        title_label = QLabel("Task Title:")
        title_label.setStyleSheet("font-size: 14px;")
        self.task_title = QLineEdit()
        self.task_title.setPlaceholderText("Enter task title")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.task_title)
        assign_layout.addLayout(title_layout)
        
        # Task Description Input.
        description_label = QLabel("Task Description:")
        description_label.setStyleSheet("font-size: 14px;")
        self.task_description = QTextEdit()
        self.task_description.setPlaceholderText("Enter task description...")
        assign_layout.addWidget(description_label)
        assign_layout.addWidget(self.task_description)
        
        # Assign Task Button.
        assign_button = QPushButton("Assign Task")
        assign_button.setStyleSheet("margin-top: 5px;")
        assign_button.clicked.connect(self.assign_task)
        assign_layout.addWidget(assign_button)
        
        # --- Panel for "Manage User Roles" ---
        self.roles_panel = QWidget()
        roles_layout = QVBoxLayout()
        roles_layout.setContentsMargins(0,0,0,0)
        roles_layout.setSpacing(10)
        self.roles_panel.setLayout(roles_layout)
        
        manage_header_label = QLabel("Manage User")
        manage_header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d2d2d;")
        roles_layout.addWidget(manage_header_label)
        
        # Role: Select User.
        role_user_layout = QHBoxLayout()
        role_user_label = QLabel("Select User:")
        role_user_label.setStyleSheet("font-size: 14px;")
        self.role_user_combo = QComboBox()
        self.role_user_combo.setStyleSheet("QComboBox { padding: 4px; }")
        self.role_user_combo.addItems(users)
        role_user_layout.addWidget(role_user_label)
        role_user_layout.addWidget(self.role_user_combo)
        roles_layout.addLayout(role_user_layout)
        
        # Role: Select Role.
        role_layout = QHBoxLayout()
        role_label = QLabel("Select Role:")
        role_label.setStyleSheet("font-size: 14px;")
        self.role_combo = QComboBox()
        self.role_combo.setStyleSheet("QComboBox { padding: 4px; }")
        self.role_combo.addItems(["user", "admin"])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        roles_layout.addLayout(role_layout)
        
        # Update Role Button.
        update_role_button = QPushButton("Update Role")
        update_role_button.setStyleSheet("margin-top: 5px;")
        update_role_button.clicked.connect(self.update_role)
        roles_layout.addWidget(update_role_button)
                
        # --- Panel for "Manage User Roles" ---
        self.roles_panel = QWidget()
        roles_layout = QVBoxLayout()
        roles_layout.setContentsMargins(0, 0, 0, 0)
        roles_layout.setSpacing(10)
        self.roles_panel.setLayout(roles_layout)

        manage_header_label = QLabel("Manage User")
        manage_header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d2d2d;")
        roles_layout.addWidget(manage_header_label)

        # Role: Select User.
        role_user_layout = QHBoxLayout()
        role_user_label = QLabel("Select User:")
        role_user_label.setStyleSheet("font-size: 14px;")
        self.role_user_combo = QComboBox()
        self.role_user_combo.setStyleSheet("QComboBox { padding: 4px; }")
        self.role_user_combo.addItems(users)
        role_user_layout.addWidget(role_user_label)
        role_user_layout.addWidget(self.role_user_combo)
        roles_layout.addLayout(role_user_layout)

        # Role: Select Role.
        role_layout = QHBoxLayout()
        role_label = QLabel("Select Role:")
        role_label.setStyleSheet("font-size: 14px;")
        self.role_combo = QComboBox()
        self.role_combo.setStyleSheet("QComboBox { padding: 4px; }")
        self.role_combo.addItems(["user", "admin"])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        roles_layout.addLayout(role_layout)

        # Update Role Button.
        update_role_button = QPushButton("Update Role")
        update_role_button.setStyleSheet("margin-top: 5px;")
        update_role_button.clicked.connect(self.update_role)
        roles_layout.addWidget(update_role_button)

        # --- Section 2: Delete User ---
        delete_user_section = QGroupBox("Delete User")  # Add a titled section
        delete_user_layout = QVBoxLayout()
        delete_user_section.setLayout(delete_user_layout)

        # Delete: Select User
        delete_user_layout_inner = QHBoxLayout()
        delete_user_label = QLabel("Select User:")
        delete_user_label.setStyleSheet("font-size: 14px;")
        self.delete_user_combo = QComboBox()
        self.delete_user_combo.setStyleSheet("QComboBox { padding: 4px; }")
        self.delete_user_combo.addItems(users)
        delete_user_layout_inner.addWidget(delete_user_label)
        delete_user_layout_inner.addWidget(self.delete_user_combo)
        delete_user_layout.addLayout(delete_user_layout_inner)

        # Delete User Button
        delete_user_button = QPushButton("Delete User")
        delete_user_button.setStyleSheet("margin-top: 5px;")
        delete_user_button.clicked.connect(self.delete_user)  # Connect to delete_user method
        delete_user_layout.addWidget(delete_user_button)

        roles_layout.addWidget(delete_user_section)

        #-----Manage task panel-----
        self.manage_task_panel = QWidget()
        layout = QVBoxLayout()
        self.manage_task_panel.setLayout(layout)
        header = QLabel("Manage Tasks")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        layout.addWidget(header)

        # Search bar row for username.
        search_layout = QHBoxLayout()
        self.task_search_username_field = QLineEdit()
        self.task_search_username_field.setPlaceholderText("Search task by username...")
        search_layout.addWidget(self.task_search_username_field)

        self.task_search_title_field = QLineEdit()
        self.task_search_title_field.setPlaceholderText("Optional: Search task by title...")
        search_layout.addWidget(self.task_search_title_field)

        self.task_search_button = QPushButton("Search")
        self.task_search_button.clicked.connect(self.perform_task_search)
        search_layout.addWidget(self.task_search_button)
        
        layout.addLayout(search_layout)

        # List widget to display tasks.
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Buttons for deleting and refreshing tasks.
        btn_layout = QHBoxLayout()
        self.task_delete_button = QPushButton("Delete Selected Task")
        self.task_delete_button.clicked.connect(self.delete_selected_task)
        btn_layout.addWidget(self.task_delete_button)
        self.task_refresh_button = QPushButton("Refresh Tasks")
        self.task_refresh_button.clicked.connect(self.load_all_tasks)
        btn_layout.addWidget(self.task_refresh_button)
        layout.addLayout(btn_layout)

        # Add both panels to the main layout (only one visible at a time).
        self.main_layout.addWidget(self.assign_panel)
        self.main_layout.addWidget(self.roles_panel)
        self.main_layout.addWidget(self.manage_task_panel)
        
        # Start with the Assign Task panel visible.
        self.assign_panel.show()
        self.roles_panel.hide()
        self.manage_task_panel.hide()

    def show_assign_panel(self):
        self.assign_panel.show()
        self.roles_panel.hide()
        self.manage_task_panel.hide()

    def show_users_panel(self):
        self.assign_panel.hide()
        self.roles_panel.show()
        self.manage_task_panel.hide()

    def show_manage_task_panel(self):
        self.assign_panel.hide()
        self.roles_panel.hide()
        self.manage_task_panel.show()
        self.load_all_tasks()
    
    def assign_task(self):
        user = self.user_combo.currentText()
        title = self.task_title.text().strip()
        description = self.task_description.toPlainText().strip()
        if not title or not description:
            QMessageBox.warning(self, "Input Error", "Please enter both a task title and a description.")
            return
        if self.api.assign_task(user, title, description):
            QMessageBox.information(self, "Success", f"Task assigned to {user}!")
            self.task_title.clear()
            self.task_description.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to assign task. Please try again.")
    
    def update_role(self):
        user = self.role_user_combo.currentText()
        new_role = self.role_combo.currentText()
        try:
            self.api.update_user_role(user, new_role)
            QMessageBox.information(self, "Success", f"{user}'s role updated to {new_role}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update role: {str(e)}")

    def delete_user(self):
        user = self.delete_user_combo.currentText()  # Use the correct combo box
        reply = QMessageBox.question(
                                    self, 
                                    "Confirm Deletion", 
                                    f"Are you sure you want to delete {user}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.api.delete_user(user)
                QMessageBox.information(self, "Success", f"{user} was deleted.")
                self.refresh_user_list()  # Refresh combo box after deletion
            except Exception as e:
                QMessageBox.critical(self, f"Action Failed", "Please try again later {e}.")

    def refresh_user_list(self):
        self.role_user_combo.clear()
        users = self.api.user_with_tasks()
        self.role_user_combo.addItems(users)

    def perform_task_search(self):
        """Search for tasks based on the provided username and optional task title."""
        username = self.task_search_username_field.text().strip()
        title = self.task_search_title_field.text().strip()  # Optional search term
        
        if not username:
            QMessageBox.warning(self, "Input Error", "Please enter a username to search for tasks.")
            return
        
        # Call the API method with both username and title.
        tasks = self.api.search_task(username, title)
        self.task_list.clear()
        
        if not tasks:
            QMessageBox.information(self, "Search Results", f"No tasks found for user '{username}' with title containing '{title}'.")
            return

        for task in tasks:
            if isinstance(task, dict):
                assigned_user = task.get("username", "Unknown")
                task_title = task.get("title", "Unknown")
                description = task.get("description", "No Description")
                status = task.get("status", "Pending")
                item_text = f"{assigned_user} - {task_title}: {description} (Status: {status})"
            else:
                item_text = task
            self.task_list.addItem(item_text)
            

    def load_all_tasks(self):
        self.task_list.clear()
        # Fetch all tasks; you might call a dedicated API method here.
        tasks = self.api.user_with_tasks()  # Adjust if needed.
        if not tasks:
            QMessageBox.information(self, "No Tasks", "No tasks found.")
            return
        for task in tasks:
            if isinstance(task, dict):
                assigned_user = task.get("username", "Unknown")
                task_title = task.get("title", "Unknown")
                description = task.get("description", "No Description")
                status = task.get("status", "Pending")
                item_text = f"{assigned_user} - {task_title}: {description} (Status: {status})"
            else:
                item_text = task
            self.task_list.addItem(item_text)

    def delete_selected_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a task to delete.")
            return
        selected_item = selected_items[0]

        task_data = selected_item.data(Qt.UserRole)
        if not task_data:
            QMessageBox.critical(self, "Error, Task is missing. Cannot proceed")
            return
        
        username = task_data.get("username")
        task_id = task_data.get("task_id")
        task_title = task_data.get("title")

        if not task_id or username: 
            QMessageBox.critical(self, "Error, Incompelete task data. Cannot delete.")
            return
        
        comfrimation = QMessageBox.question(
            self,
            "Comfrime Delete",
            f"Are you sure you want to delete task {task_title}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if comfrimation == QMessageBox.StandardButton.Yes:
            try: 
                success = self.api.delete_task(task_id)
                if success: 
                    QMessageBox.information(self,"Success","Task deleted succesfully!")
                    self.load_all_tasks()
                else: 
                    QMessageBox.critical(self,"Error", "API detection failed. Please try again")
            except Exception as e: 
                QMessageBox.critical(self, f"Error is {str(e)}")