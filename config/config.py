import os


def _getenv(key, default=None, mandatory=True):
    if mandatory:
        if key in os.environ or not default is None:
            return os.getenv(key, default)
        else:
            raise KeyError("environment variable '%s' not set" % key)
    if not mandatory:
        return os.getenv(key, default)


ENVIRONMENT    = _getenv('ENVIRONMENT',    default='dev')

JWT_SECRET_KEY = _getenv('JWT_SECRET_KEY', mandatory=True)

DB_CONFIG = {
    'drivername': _getenv('DB_DRIVER',    default='mysql+pymysql'),
    'host':       _getenv('DB_HOSTNAME',  default='localhost'),
    'port':       _getenv('DB_PORT',      default='3306'),
    'database':   _getenv('DB_NAME',      default='OPENXECO'),
    'username':   _getenv('DB_USERNAME',  default='openxeco'),
    'password':   _getenv('DB_PASSWORD',  mandatory=True)
}

MAIL_SERVER         = _getenv('MAIL_SERVER',     mandatory=False)
MAIL_PORT           = _getenv('MAIL_PORT',       mandatory=False)
MAIL_USERNAME       = _getenv('MAIL_USERNAME',   mandatory=False)
MAIL_PASSWORD       = _getenv('MAIL_PASSWORD',   mandatory=False)
MAIL_USE_TLS        = _getenv('MAIL_USE_TLS',    default="True")
MAIL_USE_SSL        = _getenv('MAIL_USE_SSL',    default="True")
MAIL_DEFAULT_SENDER = _getenv('MAIL_DEFAULT_SENDER', mandatory=True)

# if set the initial admin must issue a forgot password request
# this implies mail delivery is properly configured
INITIAL_ADMIN_EMAIL = _getenv('INITIAL_ADMIN_EMAIL', mandatory=False)

IMAGE_FOLDER        = _getenv('IMAGE_FOLDER',     default="/openxeco_media")

CORS_DOMAINS        = _getenv('CORS_DOMAINS',    default="localhost:*")
# remove extra spaces, remove empty items
domains = filter(len, map(str.strip, CORS_DOMAINS.split(",")))
CORS_ORIGINS = list(map(lambda d: r'(.*\.)?{}'.format(d), domains))
