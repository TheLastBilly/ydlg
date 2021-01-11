from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean())

class Mac(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mac = db.Column(db.String(18))
    ip = db.Column(db.String(16))
    admin = db.Column(db.Boolean())
    public_id = db.Column(db.String(100))