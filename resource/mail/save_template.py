import os

from flask import request
from flask_apispec import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from decorator.verify_payload import verify_payload


class SaveTemplate(MethodResource, Resource):

    def __init__(self, db):
        self.db = db

    @log_request
    @verify_payload([
        {'field': 'name', 'type': str},
        {'field': 'content', 'type': str}
    ])
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self):
        input_data = request.get_json()

        if input_data['name'] in ["new_account", "reset_password"]:
            name = input_data['name']
            with open(os.path.join(os.path.dirname(__file__), "..", "..", "template", f"{name}.html"), "r+") as f:
                f.read()
                f.seek(0)
                f.write(input_data['content'])
                f.truncate()
        else:
            return "", "404 This mail template does not exist"

        return "", "200 "
