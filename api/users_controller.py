from user import UserModel


class UsersController:
    @staticmethod
    def new(username, email, password):
        model = UserModel()
        return model.create(username, email, password)

    @staticmethod
    def index():
        model = UserModel()
        return model.all()

    @staticmethod
    def show(user_id: int):
        model = UserModel()
        return model.find(user_id)

    @staticmethod
    def search(email: str):
        model = UserModel()
        return model.find_by_email(email)

    @staticmethod
    def update(user_id: int, username: str, email: str):
        model = UserModel()
        return model.edit(user_id, username, email)

    @staticmethod
    def destroy(user_id: int):
        model = UserModel()
        return model.delete(user_id)
