import sqlite3
from typing import Dict, List, Optional


class UserRepository:
    def __init__(self, db_file: str):
        self.db_file = db_file
        with sqlite3.connect(db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                name           TEXT NOT NULL,
                email          TEXT NOT NULL,
                hashedPassword TEXT NOT NULL,
                class_code     TEXT NOT NULL
                )""")

    def _connect(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM users").fetchall()
            return [dict(row) for row in rows]

    def get_name_and_email(self) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute("SELECT name, email FROM users").fetchall()
            return [dict(row) for row in rows]

    def find_by_name(self, name: str) -> Optional[Dict]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE name = ?", (name,)
            ).fetchone()
            return dict(row) if row else None

    def create(self, name: str, email: str, hashed_password: str, class_code: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO users (name, email, hashedPassword, class_code) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, class_code),
            )
            conn.commit()

    def delete_by_name(self, name: str) -> Optional[Dict]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE name = ?", (name,)
            ).fetchone()
            if not row:
                return None
            conn.execute("DELETE FROM users WHERE name = ?", (name,))
            conn.commit()
            return dict(row)