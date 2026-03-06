import sqlite3
from typing import List, Dict, Any

class ManagerRepository:
    def __init__(self, db_file: str = "database.db"):
        self.db_file = db_file
        with self.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT NOT NULL,
                         title TEXT NOT NULL,
                         description TEXT NOT NULL,
                         time TEXT NOT NULL,
                         importance INTEGER NOT NULL
                         )""")
    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    def create(self, username: str, title: str, description: str, time: str, importance: int) -> Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO tasks(username, title, description, time, importance) VALUES (?, ?, ?, ?, ?)""",
                    (username, title, description, time, importance)
                )
                conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": e}
    def update_by_id(self, id: int, title: str, description: str, time: str, importance: int) -> Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET title = ?, description = ?, time = ?, importance = ? WHERE id = ?",
                            (title, description, time, importance, id))
                conn.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": e}
    def delete_by_id(self, id: int) -> Any | Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
                deleted_data = cursor.fetchall()
                cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
                conn.commit()
                return deleted_data[0] if deleted_data else ()
        except Exception as e:
            return {"success": False, "error": e}
    def get_all_tasks(self) -> List[Dict[str, Any]] | Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                rows = cursor.execute("SELECT * FROM tasks").fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            return {"success": False, "error": e}
    def get_all_tasks_user(self, username: str) -> List[Dict[str, Any]] | Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                rows = cursor.execute("SELECT * FROM tasks WHERE username = ?", (username,)).fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            return {"success": False, "error": e}
    def get_by_id(self, id: int) -> List[Any] | Dict[str, Any]:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
                data = cursor.fetchall()
                return data
        except Exception as e:
            return {"success": False, "error": e}