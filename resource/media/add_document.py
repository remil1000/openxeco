import base64
import datetime
import io
import os
import traceback

import PyPDF2
from flask_apispec import MethodResource
from flask_apispec import use_kwargs, doc
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from webargs import fields

from config.config import IMAGE_FOLDER
from decorator.catch_exception import catch_exception
from decorator.log_request import log_request
from decorator.verify_admin_access import verify_admin_access
from exception.error_while_saving_file import ErrorWhileSavingFile
from utils.serializer import Serializer


class AddDocument(MethodResource, Resource):

    db = None

    def __init__(self, db):
        self.db = db

    @log_request
    @doc(tags=['media'],
         description='Add a document to the media library. Return a dictionary with the data of the new object',
         responses={
             "200": {},
             "500": {"description": "An error occurred while saving the file"},
         })
    @use_kwargs({
        'filename': fields.Str(),
        'data': fields.Str(),
    })
    @jwt_required
    @verify_admin_access
    @catch_exception
    def post(self, **kwargs):

        # Create object to save

        document = {
            "filename": kwargs["name"],
            "creation_date": datetime.date.today()
        }

        document = self.db.insert(document, self.db.tables["Document"])

        # Save file in dir

        try:
            stream = io.BytesIO(base64.b64decode(kwargs["data"].split(",")[-1]))
            f = open(os.path.join(IMAGE_FOLDER, "document_" + str(document.id)), 'wb')
            f.write(stream.read())
            f.close()
        except Exception:
            self.db.delete(self.db.tables["Document"], {"id": document.id})
            traceback.print_exc()
            raise ErrorWhileSavingFile

        return Serializer.serialize(document, self.db.tables["Document"]), "200 "
