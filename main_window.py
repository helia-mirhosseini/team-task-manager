from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(400, 300)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #444;
                margin-top: 100px;
                text-align: center;
            }
        """)
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to the Main Window!")
        layout.addWidget(welcome_label)

        self.setLayout(layout)
