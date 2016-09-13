from app.models.database import db
from app.models.serialize import Serializable
from datetime import datetime

class Authorize(db.Model, Serializable):
    _serialize_blacklist = [
        'oauth_id', 
        'email', 
        'deleted_at'
    ]
    
    id = db.Column(db.BigInteger, primary_key=True)
    oauth_id = db.Column(db.String(100), default=None, nullable=True, index=True)
    name = db.Column(db.String(100), default=None, nullable=True)
    gender = db.Column(db.String(100), default=None, nullable=True)
    picture = db.Column(db.String(512), default=None, nullable=True)
    locale = db.Column(db.String(100), default=None, nullable=True)
    verified = db.Column(db.Boolean(), default=True)
    friends = db.Column(db.BigInteger, default=None, nullable=True)
    email = db.Column(db.String(120), default=None, nullable=True)
    network = db.Column(db.String(20), index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime(), default=None)

    def __init__(self, oauth_id, name, gender, locale, verified, friends, email, network, user_id):
        self.oauth_id = oauth_id
        self.name = name
        self.gender = gender
        self.locale = locale
        self.verified = verified
        self.friends = friends
        self.email = email
        self.network = network
        self.user_id = user_id
