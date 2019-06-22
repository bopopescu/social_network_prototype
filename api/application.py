from flask import Flask, request, jsonify
from helpers.exceptions import APIException
from endpoints.user import UserEndpoint
from endpoints.post import PostEndpoint
from endpoints.comment import CommentEndpoint

app = Flask(__name__)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return UserEndpoint.get_entities()

    else:
        return UserEndpoint.post(request)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id: int):
    if request.method == 'GET':
        return UserEndpoint.get(user_id)
    elif request.method == 'PUT':
        return UserEndpoint.put(user_id, request)

    else:
        return UserEndpoint.delete(user_id)


@app.route('/users/<int:user_id>/posts', methods=['GET', 'POST'])
def handle_posts(user_id: int):
    if request.method == 'GET':
        return PostEndpoint.get_user_posts(user_id)
    else:
        return PostEndpoint.post(user_id, request)


@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_post(user_id: int, post_id: int):
    if request.method == 'GET':
        return PostEndpoint.get(post_id)
    elif request.method == 'PUT':
        return PostEndpoint.put(post_id, request)
    else:
        return PostEndpoint.delete(post_id)


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments', methods=['GET', 'POST'])
def handle_comments(user_id: int, post_id: int):
    if request.method == 'GET':
        return CommentEndpoint.get_post_comments(post_id)
    else:
        return CommentEndpoint.post(post_id, request)


@app.route('/users/<int:user_id>/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_comment(user_id: int, post_id: int, comment_id: int):
    if request.method == 'GET':
        return CommentEndpoint.get(comment_id)
    elif request.method == 'PUT':
        return CommentEndpoint.put(comment_id, request)
    else:
        return CommentEndpoint.delete(comment_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
