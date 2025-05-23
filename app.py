import sys
from PyQt6.QtWidgets import QApplication
from database import Database
from login_window import LoginWindow
from admin_window import AdminWindow
from user_window import UserWindow

def main():
    db = Database()
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
    # users = db.get_user_role()
    # print("Users in DB:", users)

if __name__ == "__main__":
    main()
    

