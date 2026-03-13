from fastapi import APIRouter, Cookie
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
    async def update_task(data: Dict[str, Any], session_token: str = Cookie(None)):
        id = data.get("id", "")
        username = authService.get_username(session_token)
        title = data.get("title", "")
        description = data.get("description", "")
        time = data.get("time", "")
        importance = data.get("importance", "")

        if not (id and username and title and description and time and importance):
            return {"success": False, "error": "Заполните все поля!"}

        task_service.update_task(id, title, description, time, importance)
    @router.delete("/tasks/{id}")
    async def delete_task(id: int):
        task_service.delete_task(id)
    @router.get("/completed_tasks")
    async def get_all_completed_tasks(session_token: str = Cookie(None)):
        username = authService.get_username(session_token)

        if isinstance(username, str):
            return task_service.show_all_completed_tasks_user(username)

        return []
    @router.post("/completed_tasks/{id}")
    async def change_state_task(id: int, session_token: str = Cookie(None)):
        username = authService.get_username(session_token)
        
        if isinstance(username, str):
            return task_service.change_state_to_complete_user(id, username)

        return []
    @router.delete("/completed_tasks/{id}")
    async def delete_completed_task(id: int, session_token: str = Cookie(None)):
        username = authService.get_username(session_token)
        
        if isinstance(username, str):
            return task_service.delete_completed_task(id, username)

        return []
    return router