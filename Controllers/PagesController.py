from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates

from Services.AuthService import AuthService
pages_router = APIRouter(tags=["pages"])


def make_pages_router(managerService: AuthService, templates: Jinja2Templates, favicon_path: str) -> APIRouter:

    def _require_auth(token: str):
        username = managerService.get_username(token)

        if not username:
            return None, RedirectResponse(url="/login", status_code=302)

        return username, None
    
    @pages_router.get("/favicon.ico", response_class=FileResponse)
    async def icon():
        return FileResponse(favicon_path)
    @pages_router.get("/", response_class=HTMLResponse)
    async def home(request: Request, session_token: str = Cookie(None)):

        username, redirect = _require_auth(session_token)

        if redirect:
            return redirect

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "username": username},
        )
    @pages_router.get("/register", response_class=HTMLResponse)
    async def register_page(request: Request):

        return templates.TemplateResponse(
            "register.html",
            {"request": request},
        )
    @pages_router.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):

        return templates.TemplateResponse(
            "login.html",
            {"request": request},
        )
    @pages_router.get("/tasks", response_class=HTMLResponse)
    async def tasks_page(request: Request, session_token: str = Cookie(None)):

        username, redirect = _require_auth(session_token)

        if redirect:
            return redirect

        return templates.TemplateResponse(
            "tasks.html",
            {"request": request, "username": username},
        )
    
    return pages_router