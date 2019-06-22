from endpoints.base_endpoint import BaseEndpoint
from flask import jsonify, url_for
from controllers.posts_controller import PostsController
from helpers.exceptions import APIException


class PostEndpoint(BaseEndpoint):
    @staticmethod
    def get_entities():
        return jsonify({'data': PostsController.index()})

    @staticmethod
    def get_user_posts(user_id: int):
        return jsonify({'data': PostsController.get_user_posts(user_id)})

    @staticmethod
    def get(post_id: int):
        post = PostsController.show(post_id)
        if not post:
            raise APIException('Post not found')
        return jsonify({'data': post})

    @staticmethod
    def post(user_id: int, request_obj):
        json_data = request_obj.get_json()
        if 'title' in json_data and 'body' in json_data:
            data = {
                'user_id': user_id,
                'title': json_data['title'],
                'body': json_data['body']
            }
        else:
            raise APIException('Post title and body must be provided', status_code=400)

        post = PostsController.new(**data)
        return jsonify({'data': post}), 201, {
            'Location': url_for('handle_posts', user_id=post['user_id'], post_id=post['id'], external=True)
        }

    @staticmethod
    def put(post_id: int, request_obj):
        json_data = request_obj.get_json()
        data = {
            'title': json_data['title'],
            'body': json_data['body']
        }
        return jsonify({'data': PostsController.update(post_id, **data)})

    @staticmethod
    def delete(post_id):
        return jsonify({'data':  PostsController.destroy(post_id)})
