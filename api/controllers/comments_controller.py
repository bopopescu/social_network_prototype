from controllers.base_controller import BaseController
from models.comment import CommentModel


class CommentsController(BaseController):
    @staticmethod
    def model():
        return CommentModel()

    @staticmethod
    def new(user_id: int, post_id: int, body: str):
        return CommentsController.model().create(user_id, post_id, body)

    @staticmethod
    def index():
        return CommentsController.model().all()

    @staticmethod
    def show(comment_id: int):
        return CommentsController.model().find(comment_id)

    @staticmethod
    def update(comment_id: int, body: str):
        return CommentsController.model().edit(comment_id, body)

    @staticmethod
    def destroy(comment_id: int):
        return CommentsController.model().delete(comment_id)
