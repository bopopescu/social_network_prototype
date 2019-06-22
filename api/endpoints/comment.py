from endpoints.base_endpoint import BaseEndpoint
from flask import jsonify
from controllers.comments_controller import CommentsController
from helpers.exceptions import APIException


class CommentEndpoint(BaseEndpoint):
    @staticmethod
    def get_entities():
        return jsonify({'data': CommentsController.index()})

    @staticmethod
    def get_post_comments(post_id: int):
        return jsonify({'data': CommentsController.get_post_comments(post_id)})

    @staticmethod
    def get(comment_id: int):
        comment = CommentsController.show(comment_id)
        if not comment:
            raise APIException('Comment not found')
        return jsonify(comment)

    @staticmethod
    def post(post_id: int, request_obj):
        json_data = request_obj.get_json()
        if 'body' in json_data and 'user_id' in json_data:
            data = {
                'user_id': json_data['user_id'],
                'post_id': post_id,
                'body': json_data['body']
            }
        else:
            raise APIException('Comment body and user_id must be provided', status_code=400)
        comment = CommentsController.new(**data)
        return jsonify({'data': comment}), 201

    @staticmethod
    def put(comment_id: int, request_obj):
        json_data = request_obj.get_json()
        data = {
            'body': json_data['body']
        }
        return jsonify({'data': CommentsController.update(comment_id, **data)})

    @staticmethod
    def delete(comment_id: int):
        return jsonify({'data': CommentsController.destroy(comment_id)})
