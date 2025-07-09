from fastapi import FastAPI
from routers.tasks_router import tasks_router
"""
This module initializes the FastAPI application for the Task Manager API.

- Imports FastAPI for creating the web application.
- Imports the tasks_router from the routers package to handle task-related endpoints.
- Creates an instance of FastAPI.
- Includes the tasks_router with the prefix '/tasks' and tags it as 'tasks'.
- Defines the root endpoint ("/") that returns a welcome message for the API.
"""

app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


@app.get("/")
async def root():
    return {"message": "Task Manager API"}
