from flask import current_app
from app.models.database import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.serialize import Serializable
from datetime import datetime

class User(db.Model, UserMixin, Serializable):
    _serialize_blacklist = [
        'password',
        'email',
        'phone',
        'deleted_at',
        'updated_at'
    ]

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), default=None, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True, default=None)
    password = db.Column(db.String(120), default=None, nullable=True)
    phone = db.Column(db.String(60), default=None, nullable=True)
    picture = db.Column(db.String(30), default=None, nullable=True)
    locale = db.Column(db.String(4), default=None, nullable=True)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime(), default=None)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        if password is None:
            self.password = None
        else:
            self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_deleted(self):
        if self.deleted_at:
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_admin(self):
        if self.id in current_app.config['ADMIN_USER_IDS']:
            return True

        return False

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username
