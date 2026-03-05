from typing import List
from Repositories.ManagerRepository import ManagerRepository

class ManagerService:
    def __init__(self, managerRepository: ManagerRepository = ManagerRepository()):
        self.managerRepository = managerRepository
    def show_all_tasks(self) -> List:
        return self.managerRepository.get_all_tasks()
    def show_all_tasks_user(self, username: str) -> List:
        return self.managerRepository.get_all_tasks_user(username)
    def add_task(self, username: str, title: str, description: str, time: str, importance: int):
        self.managerRepository.create(username, title, description, time, importance)
    def update_task(self, id: int, title: str, description: str, time: str, importance: int):
        self.managerRepository.update_by_id(id, title, description, time, importance)
    def delete_task(self, id: int):
        self.managerRepository.delete_by_id(id)
    