#!/usr/bin/env python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from app import create_app
from app.models.database import db
from app.models.user import User

# default to dev config because no one should use this in production anyway
env = os.environ.get("app_ENV", "dev")
app = create_app("app.settings.%sConfig" % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server(host=app.config["HOST"], port=app.config["PORT"]))
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """
    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """
    db.create_all()

if __name__ == "__main__":
    manager.run()
