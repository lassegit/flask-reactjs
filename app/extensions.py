from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
from flask_mailgun import Mailgun
from flask_babel import Babel

from app.models.user import User

cache = Cache()

debug_toolbar = DebugToolbarExtension()

csrf = CsrfProtect()

oauth = OAuth()

mailgun = Mailgun()

babel = Babel()

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
