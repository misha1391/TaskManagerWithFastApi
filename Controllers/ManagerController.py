from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Dict, Any

app = FastAPI()

@app.get("/")
async def to_home():
    return RedirectResponse("/home", status_code=302)
@app.get("/home")
async def test():
    return {"Status": "Success"}
@app.post("/api/tasks")
async def add_task(data: Dict[str, Any]):
    username = data.get("username", "")
    title = data.get("title", "")
    description = data.get("description", "")
    time = data.get("time", "")
    importance = data.get("importance", "")

    if not (username and title and description and time and importance):
        return {"success": False, "error": "Заполните все поля!"}
    