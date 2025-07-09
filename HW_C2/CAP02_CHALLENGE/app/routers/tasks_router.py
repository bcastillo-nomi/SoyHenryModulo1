from fastapi import APIRouter, HTTPException, Query
from models import Task, UpdateTaskModel, TaskList
from db import db

tasks_router = APIRouter()


@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    """
    Create a new task.

    Args:
        task (Task): The task to be created.

    Returns:
        Task: The created task.
    """
    created_task = db.add_task(task)
    if created_task is None:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created_task



@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        Task: The requested task.

    Raises:
        HTTPException: If the task is not found.
    """
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/", response_model=TaskList)
async def get_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of tasks.

    Args:
        skip (int): Number of tasks to skip.
        limit (int): Maximum number of tasks to return.

    Returns:
        TaskList: A paginated list of tasks.
    """
    tasks = db.get_tasks(skip=skip, limit=limit)
    return TaskList(tasks=tasks)


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    """
    Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the task is not found.
    """
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}




@tasks_router.delete("/", summary="Delete all tasks")
async def delete_all_tasks(confirm: bool = False):
    """
    WARNING: This operation deletes all tasks and can be expensive for large datasets.
    Use with caution. Consider implementing authentication, batching, or pagination for safety.
    """
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmation required to delete all tasks. Pass confirm=true.")
    db.delete_all_tasks()
    return {"message": "All tasks deleted successfully"}

