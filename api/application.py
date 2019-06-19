from flask import Flask, request, jsonify, abort, url_for
from users_controller import UsersController
from exceptions import *

app = Flask(__name__)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return jsonify({'data': UsersController.index()})

    elif request.method == 'POST':
        json_data = request.get_json()
        if 'username' in json_data and 'email' in json_data and 'password' in json_data:
            data = {
                'username': json_data['username'],
                'email': json_data['email'],
                'password': json_data['password']
            }
        else:
            raise APIException('User username, email or password must be provided', status_code=400)

        if UsersController.search(data['email']):
            raise APIException('Email already taken', status_code=400)

        user = UsersController.new(**data)
        return jsonify({'data': user}), 201, {'Location': url_for('handle_user', user_id=user['id'], _external=True)}


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id: int):
    if request.method == 'GET':
        user = UsersController.show(user_id)
        if not user:
            raise APIException('user not found')
        return jsonify({'data': user})

    elif request.method == 'PUT':
        json_data = request.get_json()
        data = {
            'username': json_data['username'],
            'email': json_data['email']
        }
        return jsonify({'data': UsersController.update(user_id, **data)})

    else:
        return jsonify({'data':  UsersController.destroy(user_id)})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
