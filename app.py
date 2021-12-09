import sys

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api
from sqlalchemy.engine.url import URL
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_migrate import Migrate

try:
    from config import config
except ImportError:
    print("Please copy config.py.sample to config.py")
    sys.exit(1)

from db.db import DB


# Manage DB connection
db_uri = URL(**config.DB_CONFIG)

# Init Flask and set config
app = Flask(__name__, template_folder="template")
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ERROR_404_HELP"] = False

app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ['headers', 'cookies']
app.config["JWT_COOKIE_SECURE"] = config.ENVIRONMENT != "dev"
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["CORS_SUPPORTS_CREDENTIALS"] = True
app.config["CORS_ORIGINS"] = config.CORS_ORIGINS if config.CORS_ORIGINS else []

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS == "True"
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL == "True"
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER

app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SCHEDULER_API_ENABLED'] = False

app.config['APISPEC_SWAGGER_URL'] = '/doc/json'
app.config['APISPEC_SWAGGER_UI_URL'] = '/doc/'
app.config['APISPEC_SPEC'] = APISpec(
    title='openXeco API',
    version='v1.7',
    plugins=[MarshmallowPlugin()],
    openapi_version='2.0.0'
)

# Create DB instance and migration tool
db = DB(app)
migrate = Migrate(app, db.instance)

# Add additional plugins
cors = CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
docs = FlaskApiSpec(app)

# Init and set the resources for Flask
api = Api(app)


@app.route('/<generic>')
def undefined_route(_):
    return '', 404


if __name__ == 'app':
    from routes import set_routes
    set_routes({"api": api, "db": db, "mail": mail, "docs": docs})

if __name__ == '__main__':
    from routes import set_routes
    set_routes({"api": api, "db": db, "mail": mail, "docs": docs})

    app.debug = config.ENVIRONMENT == "dev"
    app.run(threaded=True)
