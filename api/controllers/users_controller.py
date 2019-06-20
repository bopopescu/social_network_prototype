from controllers.base_controller import BaseController
from models.user import UserModel


class UsersController(BaseController):
    @staticmethod
    def model():
        return UserModel()

    @staticmethod
    def new(username, email, password):
        return UsersController.model().create(username, email, password)

    @staticmethod
    def index():
        return UsersController.model().all()

    @staticmethod
    def show(user_id: int):
        return UsersController.model().find(user_id)

    @staticmethod
    def search(email: str):
        return UsersController.model().find_by_email(email)

    @staticmethod
    def update(user_id: int, username: str, email: str):
        return UsersController.model().edit(user_id, username, email)

    @staticmethod
    def destroy(user_id: int):
        return UsersController.model().delete(user_id)
