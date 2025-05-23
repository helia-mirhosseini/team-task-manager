from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QCheckBox,QMessageBox
from password_line_edit import PasswordLineEdit
from api_client import APIClient 


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api = APIClient()
        self.setWindowTitle("Register")
        self.resize(300, 200)
        
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
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # When Enter is pressed in the password field, attempt login.
        self.password_input.returnPressed.connect(self.register_user)
        # Checkbox to set admin role
        self.admin_checkbox = QCheckBox("Register as Admin")
        layout.addWidget(self.admin_checkbox)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)
        
    def focus_password_field(self):
        """Move focus to the password field."""
        self.password_input.setFocus()

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both a username and a password.")
            return

        role = "admin" if self.admin_checkbox.isChecked() else "user"

        try:
            self.api.insert_user(username, password, role)
            QMessageBox.information(self, "Success", "User registered successfully!")
            self.close()  # Close the registration window after successful registration
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")

    