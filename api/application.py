from flask import Flask, request, jsonify
from helpers.exceptions import APIException
from endpoints.user import UserEndpoint

app = Flask(__name__)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return UserEndpoint.get_users()

    elif request.method == 'POST':
        return UserEndpoint.post(request)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id: int):
    if request.method == 'GET':
        return UserEndpoint.get(user_id)
    elif request.method == 'PUT':
        return UserEndpoint.put(user_id, request)

    else:
        return UserEndpoint.delete(user_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
