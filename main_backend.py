from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database import Database
import requests
import logging
app = FastAPI()
db = Database()
logging.basicConfig(level=logging.DEBUG)

class User(BaseModel):
    username: str
    password: str
    role: str
    
    
class Task(BaseModel): 
    title: str
    description: str
    status: Optional[str] = 'Pending'
    
    
class UserTask(BaseModel): 
    name: str
    tasks: List[Task]

class LoginRequest(BaseModel):
    username: str
    password: str
    

        

@app.post("/users/")
async def create_user(user: User): 
    db.insert_user(user.username,user.password,user.role)
    return {"message": f"User {user.username} added successfully"}

@app.post("/tasks/")
async def assign_task(username : str, task : Task):
    db.assign_task(username, task.title, task.description)
    return {"message": f"Task '{task.title}' assigned to {username}."}

@app.get("/tasks/")
async def search_task(username: str, title:Optional[str] = None):
    try:
        tasks = db.search_task(username,title)

        if tasks is None:
            raise HTTPException(status_code=404, detail="User not found.")

        if not tasks:  # User exists but has no tasks
            raise HTTPException(status_code=404, detail="No tasks assigned to this user.")

        return {
            "user": username,
            "task": [  # Wrap tasks in "task" key
                {"title": t[0], "description": t[1], "status": t[2]} for t in tasks
            ]
        }
    except Exception as e: 
        logging.error(f"Error occured while searching task: {str(e)}")
        raise HTTPException(status_code= 500 , detail= "Internal Server Error")


@app.put("/tasks/{task_id}/status")
async def update_status( task_id: int, new_status: str): 
    db.update_task_status(task_id, new_status)
    return {"message":f"Task {task_id} status updated to {new_status}."}

@app.delete("/users/{username}/")
async def delete_user(username: str):
    db.delete_user(username)
    return{"message":f"user {username} was deleted."}
    

@app.delete("/tasks/{task_title}/")
async def delete_task( task_title: str):
    db.delete_task(task_title)
    return{"message":f"task {task_title} was deleted."}

@app.get("/users/tasks/")
async def show_all_member_with_tasks():
    users_tasks = db.user_with_tasks()
    return{"users with tasks": users_tasks}


@app.get("/users/")
async def login(username, password):
    user_data = db.check_user_credentials(username, password)
    
    if not user_data:  # If user_data is None or empty
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"role": user_data["role"]}
