from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit, QToolButton

class PasswordLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Start with password hidden
        self.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Create the eye button as a child of the QLineEdit
        self.eye_button = QToolButton(self)
        self.eye_button.setIcon(QIcon("eye_icon.jpg"))  # Replace with your icon path if needed.
        self.eye_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button.setStyleSheet("border: none; background: transparent;")
        self.eye_button.setFixedSize(20, 20)
        
        # Connect the button pressed and released events.
        self.eye_button.pressed.connect(self.show_password)
        self.eye_button.released.connect(self.hide_password)
        
        # Add some right text margin so that text doesn't flow under the button.
        margin = self.eye_button.width() + 4
        self.setTextMargins(0, 0, margin, 0)

    def resizeEvent(self, event):
        """Reposition the eye button when the QLineEdit is resized."""
        super().resizeEvent(event)
        button_width = self.eye_button.width()
        button_height = self.eye_button.height()
        x = self.rect().right() - button_width - 2
        y = (self.rect().height() - button_height) // 2
        self.eye_button.move(x, y)

    def show_password(self):
        """Display the password in normal text."""
        self.setEchoMode(QLineEdit.EchoMode.Normal)

    def hide_password(self):
        """Mask the password input."""
        self.setEchoMode(QLineEdit.EchoMode.Password)
