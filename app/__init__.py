#! ../env/bin/python

from flask import Flask, request, g, redirect
from logging.handlers import RotatingFileHandler
import logging

# Controllers
from app.models.database import db
from app.controllers.main import main
from app.controllers.profile import profile
from app.controllers.auth import auth
from app.controllers.authorize import authorize

# Api controllers

# External controllers

# Misc
from app.tpl_filter import tpl_filter
from app.extensions import (
    cache,
    debug_toolbar,
    login_manager,
    csrf,
    oauth,
    mailgun,
    babel
)

def create_app(object_name, env='prod'):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object, e.g. app.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """
    app = Flask(__name__, static_url_path='')

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # templates and statics
    app.template_folder = app.config['TEMPLATE_FOLDER']
    app.static_folder = app.config['STATIC_FOLDER']

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # CSRF protection
    csrf.init_app(app)

    # Oauthlib
    oauth.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    # Authentication
    login_manager.init_app(app)

    # Mailgun
    mailgun.init_app(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(profile)
    app.register_blueprint(authorize)

    # Api

    # Extneral

    # Import custom template filters
    app.register_blueprint(tpl_filter)

    # Enable error logging
    # if app.config['ENV'] == 'prod':
    #     file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    #     formatter = logging.Formatter( "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    #     file_handler.setFormatter(formatter)
    #     app.logger.addHandler(file_handler)

    # Language
    babel.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     return g.locale

    # # Set lang
    # @app.before_request
    # def before_request():
    #     lang_cookie = request.cookies.get('locale')
    #     locale = lang_cookie if lang_cookie else 'en'

    #     if not lang_cookie:
    #         for lang in request.accept_languages.values():
    #             if lang[:2] in ['de', 'en']:
    #                 locale = lang[:2]
    #                 break

    #     g.locale = locale

    return app
