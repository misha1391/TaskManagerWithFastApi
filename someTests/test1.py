from ..Repositories.ManagerRepository import ManagerRepository

database = ManagerRepository()
database.create("Title", "RandomUser", "Some description", "10:00", 3)
print(database.get_by_id(0))
database.delete_by_id(0)