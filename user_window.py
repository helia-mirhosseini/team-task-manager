from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
from PyQt6.QtCore import Qt
from api_client import APIClient

class UserWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.api = APIClient()
        self.setWindowTitle(f"Dashboard {username}")  # "Dashboard" in Persian
        self.resize(500, 400)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Ariel',sans-serif;  /* Replace with your Persian font */
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
        header_label = QLabel("You're Tasks")  # "Your Tasks" in Persian
        # header_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(header_label)

        # Task List
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Buttons
        refresh_button = QPushButton("Refresh Tasks")  # "Refresh Tasks" in Persian
        complete_button = QPushButton("Marked as Complete")  # "Mark as Complete" in Persian
        layout.addWidget(refresh_button)
        layout.addWidget(complete_button)

        self.setLayout(layout)
        self.load_tasks()

    def load_tasks(self):

         pass
