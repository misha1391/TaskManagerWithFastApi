from typing import List, Dict, Any
from Repositories.ManagerRepository import ManagerRepository

class ManagerService:
    def __init__(self, managerRepository: ManagerRepository = ManagerRepository()):
        self.managerRepository = managerRepository
    def show_all_tasks(self) -> List[Dict[str, Any]] | Dict[str, Any]:
        return self.managerRepository.get_all_tasks()
    def show_all_tasks_user(self, username: str) -> List[Dict[str, Any]] | Dict[str, Any]:
        return self.managerRepository.get_all_tasks_user(username)
    def add_task(self, username: str, title: str, description: str, time: str, importance: int) -> Dict[str, Any]:
        return self.managerRepository.create(username, title, description, time, importance)
    def update_task(self, id: int, title: str, description: str, time: str, importance: int):
        return self.managerRepository.update_by_id(id, title, description, time, importance)
    def delete_task(self, id: int):
        return self.managerRepository.delete_by_id(id)
    def show_all_completed_tasks_user(self, username: str):
        return self.managerRepository.get_all_completed_tasks_user(username)
    def change_state_to_complete_user(self, id: int, username: str):
        if self.managerRepository.can_user_change_id(id, username):
            return self.managerRepository.change_state_to_completed(id)
        
        return {"success": False, "error": "Authorization required"}
    def delete_completed_task(self, id: int, username: str):
        if self.managerRepository.can_user_change_id_completed(id, username):
            return self.managerRepository.delete_by_id_completed(id)
        
        return {"success": False, "error": "Authorization required"}
