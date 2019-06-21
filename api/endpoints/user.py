from endpoints.base_endpoint import BaseEndpoint
from flask import jsonify, url_for
from controllers.users_controller import UsersController
from helpers.exceptions import APIException


class UserEndpoint(BaseEndpoint):
    @staticmethod
    def get_entities():
        return jsonify({'data': UsersController.index()})

    @staticmethod
    def get(user_id: int):
        user = UsersController.show(user_id)
        if not user:
            raise APIException('User not found')
        return jsonify({'data': user})

    @staticmethod
    def post(request_obj):
        json_data = request_obj.get_json()
        if 'username' in json_data and 'email' in json_data and 'password' in json_data:
            data = {
                'username': json_data['username'],
                'email': json_data['email'],
                'password': json_data['password']
            }
        else:
            raise APIException('User username, email and password must be provided', status_code=400)

        if UsersController.search(data['email']):
            raise APIException('Email already taken', status_code=400)

        user = UsersController.new(**data)
        return jsonify({'data': user}), 201, {'Location': url_for('handle_user', user_id=user['id'], external=True)}

    @staticmethod
    def put(user_id, request_obj):
        json_data = request_obj.get_json()
        data = {
            'username': json_data['username'],
            'email': json_data['email']
        }
        return jsonify({'data': UsersController.update(user_id, **data)})

    @staticmethod
    def delete(user_id: int):
        return jsonify({'data':  UsersController.destroy(user_id)})
