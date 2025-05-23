import sqlite3
import hashlib
import bcrypt


class Database:
    def __init__(self, db_username='database.db'):
        self.db_username = db_username
        self.create_tables()

    def get_connection(self):
        """Get the connection to the SQLite database."""
        conn = sqlite3.connect(self.db_username, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')  # Enable Write-Ahead Logging for concurrency
        return conn
    
    

    def create_tables(self):
        """Create the tables if they don't already exist."""
        conn = self.get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()

    def insert_user(self, username, password, role):
        """Create a new user with the provided username, password, and role."""
        conn = self.get_connection()
        c = conn.cursor()

        # Insert user data (username, password, and role) as plain text
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        
        return {"message": f"User {username} added successfully!"}
    

    
    def update_password(self, username, new_password):
        """Update the password for the user in the database."""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Update the user's password with the new plain-text password
        c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()

        return {"message": f"Password for {username} updated successfully!"}


    def check_user_credentials(self, username, password):
        """Check user credentials and return the user role if valid."""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Fetch stored password and role from the database based on username
        c.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_password, role = user  # Extract values from the result
            
            # Directly compare the entered password with the stored password
            if stored_password == password:
                return {"role": role}  # Passwords match, return user role
            else:
                return None  # Incorrect password
        return None  # User not found

    
    def get_user_role(self, username):
        """Get the role of a user."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username = ?", (username,))
        role = c.fetchone()
        conn.close()
        return role[0] if role else None
    
    def update_user_role(self, username, new_role):
        """Update the role of an existing user."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        conn.close()
        print(f"User {username} role updated to {new_role}.")

    def assign_task(self, username, title, description, status='Pending'):
        """Assign a task to a user."""
        conn = self.get_connection()
        c = conn.cursor()

        # Fetch user_id from users table
        c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()

        if not user_id:
            raise ValueError("User not found.")

        # Check if the task already exists to prevent duplicate entries
        c.execute("""
            SELECT * FROM tasks WHERE user_id = ? AND title = ?
        """, (user_id[0], title))

        existing_task = c.fetchone()

        if existing_task:
            print(f"Task '{title}' already assigned to {username}. Skipping insert.")
            return

        # Insert the task if it doesn't exist
        c.execute("""
            INSERT INTO tasks (user_id, title, description, status)
            VALUES (?, ?, ?, ?)
        """, (user_id[0], title, description, status))

        conn.commit()

    def search_task(self, username, title):
        """Search for tasks assigned to a user by matching task titles partially."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT tasks.title, tasks.description, tasks.status
            FROM tasks
            LEFT JOIN users ON tasks.user_id = users.user_id
            WHERE users.username = ? AND tasks.title LIKE ?
        """, (username, f"%{title}%"))
        tasks = c.fetchall()
        return tasks

    def fetch_task_id(self, username, task_title):
        """Fetch the task_id based on username and exact task title."""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT task_id FROM tasks
                LEFT JOIN users ON tasks.user_id = users.user_id
                WHERE users.username = ? AND tasks.title = ?
            """, (username, task_title))
            task_id = c.fetchone()
        return task_id[0] if task_id else None


    def update_task_status(self, task_id, new_status):
        """Update the status of a task."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (new_status, task_id))
        conn.commit()
        print(f"Task ID {task_id} status updated to {new_status}.")

    def delete_user(self, username):
        """Delete a user from the database."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT user_id FROM users WHERE username =?',(username,))
        result = c.fetchone()
        if result :
            user_id  = result[0]
            c.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            # print(f'User {username} deleted.')

    def delete_task(self, task_title):
        """Delete a task from the database."""
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT task_id FROM tasks WHERE title = ?', (task_title,))
        result = c.fetchone()
        if result: 
            tasks_id = result[0]        
            c.execute('DELETE FROM tasks WHERE task_id = ?', (tasks_id,))
            conn.commit()
            # print(f'Task {task_title} deleted.')

    def user_with_tasks(self):
        """Get all users with their tasks."""
        conn = self.get_connection()
        c = conn.cursor()

        c.execute("""
            SELECT users.username, tasks.title, tasks.description, tasks.status
            FROM users
            LEFT JOIN tasks ON users.user_id = tasks.user_id
            ORDER BY users.username;
        """)

        results = c.fetchall()
        users = []
        if results:
            current_user = None
            for row in results:
                username, task_title, task_description, task_status = row
                if username != current_user:
                    current_user = username
                    users.append(username)
                    print(f"\n{username}'s Tasks:")

                if task_title:
                    print(f"   - {task_title}: {task_description} (Status: {task_status})")
                else:
                    print("   - No tasks assigned.")
        else:
            print("No users found in the database.")
        return users
