from typing import Dict, Any

from fastapi import APIRouter, Cookie, Response
from fastapi.responses import RedirectResponse

from Services.AuthService import AuthService

router = APIRouter(prefix="/api", tags=["auth"])


def make_auth_router(auth_service: AuthService) -> APIRouter:
    @router.post("/register")
    async def register(data: Dict[str, Any]):
        return auth_service.register(
            username=data.get("username", "").strip(),
            password=data.get("password", ""),
            email=data.get("email", ""),
            class_code=data.get("class_code", ""),
        )
    @router.post("/login")
    async def login(data: Dict[str, Any], response: Response):
        token = auth_service.login(
            username=data.get("username", "").strip(),
            password=data.get("password", ""),
        )
        if not token:
            return {"success": False, "error": "Неверное имя пользователя или пароль"}
        response.set_cookie(key="session_token", value=token, httponly=True)
        return {"success": True}
    @router.post("/logout")
    async def logout(response: Response, session_token: str = Cookie(None)):
        if session_token:
            auth_service.destroy_session(session_token)
        response.delete_cookie("session_token")
        return RedirectResponse(url="/login", status_code=302)
    @router.get("/check_auth")
    async def check_auth(session_token: str = Cookie(None)):
        username = check_auth(session_token)
        if username:
            return {"authenticated": True, "username": username}
        return {"authenticated": False}
    return router