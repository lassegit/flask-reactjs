from app.models.database import db
from app.models.serialize import Serializable
from datetime import datetime

class Password_reset(db.Model):
    _serialize_blacklist = [
        'token', 
        'email'
    ]
    
    token = db.Column(db.String(44), primary_key=True)
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, token, email):
        self.token = token
        self.email = email
