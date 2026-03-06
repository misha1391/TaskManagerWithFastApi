import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from Repositories.UserRepository import UserRepository
from Repositories.ManagerRepository import ManagerRepository
from Services.AuthService import AuthService
from Services.ManagerService import ManagerService
from Controllers.AuthController import make_auth_router
from Controllers.PagesController import make_pages_router
from Controllers.ManagerController import make_tasks_router

DB_FILE = "database.db"

user_repo    = UserRepository(DB_FILE)
auth_service = AuthService(user_repo)
task_repo    = ManagerRepository(DB_FILE)
task_service = ManagerService(task_repo)
templates    = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(make_auth_router(auth_service))
app.include_router(make_pages_router(auth_service, templates))
app.include_router(make_tasks_router(auth_service, task_service))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")