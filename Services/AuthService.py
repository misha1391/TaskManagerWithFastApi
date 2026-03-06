import hashlib
import secrets
from typing import Dict, Optional

from Repositories.UserRepository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self._sessions: Dict[str, str] = {}  # token -> username

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(32)

    # --- Сессии ---

    def get_username(self, token: Optional[str]) -> Optional[str]:
        if not token:
            return None
        return self._sessions.get(token)

    def create_session(self, username: str) -> str:
        token = self.generate_token()
        self._sessions[token] = username
        return token

    def destroy_session(self, token: str) -> None:
        self._sessions.pop(token, None)

    # --- Регистрация ---

    def register(self, username: str, password: str, email: str, class_code: str) -> Dict:
        if not all([username, password, email, class_code]):
            return {"success": False, "error": "Заполните все поля"}
        if self.user_repo.find_by_name(username):
            return {"success": False, "error": "Пользователь уже существует"}
        self.user_repo.create(
            name=username,
            email=email,
            hashed_password=self.hash_password(password),
            class_code=class_code,
        )
        return {"success": True}

    # --- Вход ---

    def login(self, username: str, password: str) -> Optional[str]:
        """Возвращает токен при успехе, иначе None."""
        if not username or not password:
            return None
        user = self.user_repo.find_by_name(username)
        if user and user["hashedPassword"] == self.hash_password(password):
            return self.create_session(username)
        return None