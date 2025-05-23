from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from register_window import RegisterWindow
from password_line_edit import PasswordLineEdit
from admin_window import AdminWindow
from user_window import UserWindow
from api_client import APIClient  # Assuming your APIClient class is properly set up for login
import asyncio

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api = APIClient()
        self.setWindowTitle("Login")
        self.resize(300, 200)

        # Apply styles for the window
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                border: 1px solid #bbb;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                background-color: white;   /* Neutral background for text fields */
                color: black;              /* High contrast text color */
            }
            QPushButton {
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            
            QPushButton {
                background-color: #d76e38;
                border: 1px solid #d76e38;
            }
            QPushButton:hover {
                background-color: #c9582d;
                border: 1px solid #c9582d;
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #c9582d, stop: 1 #a74327
                );
                border: 1px solid #863726;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
        """)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # When the user presses Enter in the username field, move focus to password.
        self.username_input.returnPressed.connect(self.focus_password_field)
        
        self.password_input = PasswordLineEdit()
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)

        # When Enter is pressed in the password field, attempt login.
        self.password_input.returnPressed.connect(self.login_user)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_user)
        layout.addWidget(login_button)

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.open_signup)
        layout.addWidget(signup_button)

        self.setLayout(layout)

    def focus_password_field(self):
        """Move focus to the password field."""
        self.password_input.setFocus()
        
    def login_user(self):
        """Handle the user login."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Call API client to validate login
        role = self.api.login(username, password)  # Assuming your APIClient class handles login

        if role is None:  # API call failed, or user is not found
            QMessageBox.critical(self, "Error", "Invalid credentials!")
            return

        if role == "admin":
            QMessageBox.information(self, "Login Successful", f"Welcome {username} (Admin)!")
            self.admin_window = AdminWindow()
            self.admin_window.show()
        elif role== "user":
            QMessageBox.information(self, "Login Successful", f"Welcome {username} (User)!")
            self.user_window = UserWindow(username)
            self.user_window.show()
        else:
            QMessageBox.critical(self, "Error", "Invalid role!")
            return

        self.close()  # Close the login window once the user is authenticated

    def open_signup(self):
        """Open the sign-up window."""
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
