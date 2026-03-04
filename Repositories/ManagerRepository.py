import sqlite3

class ManagerRepository:
    def __init__(self, database_file: str = "database.db"):
        self.database_file = database_file
        with self.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT NOT NULL,
                         title TEXT NOT NULL,
                         description TEXT NOT NULL,
                         time TEXT NOT NULL,
                         importance INTEGER NOT NULL
                         )""")
    def connect(self):
        conn = sqlite3.connect(self.database_file)
        return conn
    def create(self, username: str, title: str, description: str, time: str, importance: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO tasks (username, title, description, time, importance) VALUES (?, ?, ?, ?, ?)""",
                (username, title, description, time, importance)
            )
            conn.commit()
    def update_by_id(self, id: int, title: str, description: str, time: str, importance: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET title = ?, description = ?, time = ?, importance = ? WHERE id = ?",
                        (title, description, time, importance, id))
            conn.commit()
    def delete_by_id(self, id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            deleted_data = cursor.fetchall()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
            conn.commit()
            return deleted_data[0] if deleted_data else ()
    def get_all_tasks(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM tasks").fetchall()
            return [dict(row) for row in rows]
    def get_by_id(self, id: int):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
            data = cursor.fetchall()
            return data