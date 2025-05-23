import pytest
from fastapi.testclient import TestClient
from main_backend import app
from database import Database
from unittest.mock import patch

@pytest.fixture
def client():
    db = Database()
    
    # Clean up users and tasks before each test
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks")
    c.execute("DELETE FROM users")
    conn.commit()
    
    return TestClient(app)

# Test for creating users
def test_create_user(client):
    response = client.post("/users/", json={"name": "user1", "password": "password1"})
    assert response.status_code == 200
    assert response.json() == {"message": "User user1 added successfully"}

    response = client.post("/users/", json={"name": "user2", "password": "password2"})
    assert response.status_code == 200
    assert response.json() == {"message": "User user2 added successfully"}

# Test for assigning a task
def test_assign_task(client):
    # Ensure the user exists before assigning tasks
    client.post("/users/", json={"name": "user1", "password": "password1"})
    response = client.post("/tasks/", params={"user_name": "user1"}, json={"title": "task1", "description": "test task"})
    assert response.status_code == 200
    assert response.json() == {"message": "Task 'task1' assigned to user1."}

# Test for getting user tasks
def test_get_user_tasks(client):
    client.post("/users/", json={"name": "user1", "password": "password1"})
    
    # Ensure only one post for "task1"
    client.post("/tasks/", params={"user_name": "user1"}, json={"title": "task1", "description": "test task"})
    client.post("/tasks/", params={"user_name": "user1"}, json={"title": "task2", "description": "test task"})

    response = client.get("/tasks/user1/")
    actual_response = response.json()
    print("Actual Response:", actual_response)  # Debugging output

    expected_response = {
        "user": "user1",
        "task": [
            {"title": "task1", "description": "test task", "status": "Pending"},
            {"title": "task2", "description": "test task", "status": "Pending"}
        ]
    }
    
    assert response.status_code == 200
    assert actual_response == expected_response


# Test for getting user tasks with no tasks assigned
def test_get_user_tasks_no_task(client):
    # Ensure user2 exists but no tasks assigned
    client.post("/users/", json={"name": "user2", "password": "password2"})
    response = client.get("/tasks/user2/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No tasks assigned to this user."}

def test_update_task_status(client):
    # Prepare the task ID and new status
    task_id = 1
    new_status = "Completed"

    # Perform the PUT request to update the task status
    response = client.put(f"/tasks/{task_id}/status?new_status={new_status}")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response body contains the correct message
    assert response.json() == {"message": f"Task {task_id} status updated to {new_status}."}

def test_delete_member(client):
    user_name = "Helia Mirhosseini"
    response = client.delete(f"/users/{user_name}")
    assert response.status_code ==200
    assert response.json() == {"message":f"user {user_name} was deleted."}
    
def test_delete_task(client):
    task_title = "clean"
    response = client.delete(f"/tasks/{task_title}")
    assert response.status_code ==200
    assert response.json() == {"message":f"task {task_title} was deleted."}



def test_show_all_member_with_tasks_mocked(client):
    mock_data = [
        {"user_id": 1, "tasks": ["Task 1", "Task 2"]},
        {"user_id": 2, "tasks": ["Task A", "Task B"]}
    ]

    with patch("main.db.user_with_tasks", return_value=mock_data):
        response = client.get("/users/tasks/")
        
        # Ensure status code is correct
        assert response.status_code == 200

        # Ensure response matches expected structure
        assert response.json() == {"users with tasks": mock_data}

def test_login(client): 
    mock_data = []