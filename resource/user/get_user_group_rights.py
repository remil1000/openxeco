from flask_restful import Resource
from flask_jwt_extended import jwt_required
from db.db import DB
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from utils.serializer import Serializer


class GetUserGroupRights(Resource):

    def __init__(self, db: DB):
        self.db = db

    @log_request
    @catch_exception
    @jwt_required
    @verify_admin_access
    def get(self, id):

        data = self.db.get(self.db.tables["UserGroupRight"], {"group_id": id})
        data = Serializer.serialize(data, self.db.tables["UserGroupRight"])

        return data, "200 "
