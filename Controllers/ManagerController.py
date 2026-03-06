from fastapi import APIRouter, Request, Response, Cookie
from fastapi.responses import RedirectResponse
from typing import Dict, Any
from Services.ManagerService import ManagerService

router = APIRouter(prefix="/api", tags=["tasks"])

def make_tasks_router(task_service: ManagerService) -> APIRouter:
    @router.get("/tasks")
    async def get_all_tasks(data: Dict[str, Any]):
        username = data.get("username", "").strip()
        return task_service.show_all_tasks_user(username)
    @router.post("/tasks")
    async def add_task(data: Dict[str, Any]):
        username = data.get("username", "")
        title = data.get("title", "")
        description = data.get("description", "")
        time = data.get("time", "")
        importance = data.get("importance", "")

        if not (username and title and description and time and importance):
            return {"success": False, "error": "Заполните все поля!"}
        
        task_service.add_task(username, title, description, time, importance)
    @router.put("/tasks")
    async def update_task(data: Dict[str, Any]):
        id = data.get("id", "")
        username = data.get("username", "")
        title = data.get("title", "")
        description = data.get("description", "")
        time = data.get("time", "")
        importance = data.get("importance", "")

        if not (username and title and description and time and importance):
            return {"success": False, "error": "Заполните все поля!"}
        
        task_service.update_task(id, title, description, time, importance)
    @router.delete("/tasks")
    async def delete_task(data: Dict[str, Any]):
        id = data.get("id", "")
        task_service.delete_task(id)
    return router