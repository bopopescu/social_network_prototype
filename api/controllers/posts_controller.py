from controllers.base_controller import BaseController
from models.post import PostModel


class PostsController(BaseController):
    @staticmethod
    def model():
        return PostModel()

    @staticmethod
    def new(user_id: int, title: str, body: str):
        return PostsController.model().create(user_id, title, body)

    @staticmethod
    def index():
        return PostsController.model().all()

    @staticmethod
    def show(post_id: int):
        return PostsController.model().find(post_id)

    @staticmethod
    def update(post_id: int, title: str, body: str):
        return PostsController.model().edit(post_id, title, body)

    @staticmethod
    def destroy(post_id: int):
        return PostsController.model().delete(post_id)
