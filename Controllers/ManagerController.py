from fastapi import APIRouter, Request, Response, Cookie
from fastapi.responses import RedirectResponse
from typing import List, Dict, Any
from Services.ManagerService import ManagerService
from Services.AuthService import AuthService

router = APIRouter(prefix="/api", tags=["tasks"])

def make_tasks_router(authService: AuthService, task_service: ManagerService) -> APIRouter:
    @router.get("/tasks")
    async def get_all_tasks(session_token: str = Cookie(None)) -> List[Dict[str, Any]] | Dict[str, Any]:
        username = authService.get_username(session_token)
        if isinstance(username, str):
            return task_service.show_all_tasks_user(username)
        else:
            return []
    @router.post("/tasks")
    async def add_task(data: Dict[str, Any], session_token: str = Cookie(None)) -> Dict[str, Any]:
        username = authService.get_username(session_token)
        title = data.get("title", "")
        description = data.get("description", "")
        time = str(data.get("time", ""))
        time = time.replace("T", " ")
        importance = data.get("importance", "")

        if not (username and title and description and time and importance):
            return {"success": False, "error": "Заполните все поля!"}

        return task_service.add_task(username, title, description, time, importance)
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
    @router.delete("/tasks/{id}")
    async def delete_task(id: int):
        task_service.delete_task(id)
    return router