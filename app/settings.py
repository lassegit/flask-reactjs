import tempfile
db_file = tempfile.NamedTemporaryFile()

class Config(object):
    SECRET_KEY = 'secret key'

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    MAILGUN_DOMAIN = ''
    MAILGUN_API_KEY = ''
    MAILGUN_DEFAULT_FROM = 'Your name <noreply@domain.com>'

    CONTACT_MAIL = 'contact@domain.com'

    ADMIN_USER_IDS = [1] # Admin user id

    PORT = '5001'
    HOST = '127.0.0.1'

class ProdConfig(Config):
    DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_POOL_TIMEOUT = 30

    CACHE_TYPE = 'simple'

    STATIC_FOLDER = 'build'
    TEMPLATE_FOLDER = 'build'

class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SEND_FILE_MAX_AGE_DEFAULT = 0

    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/testdb'
    SQLALCHEMY_POOL_TIMEOUT = 30

    CACHE_TYPE = 'simple'

    STATIC_FOLDER = 'static/dev'
    TEMPLATE_FOLDER = 'templates'




