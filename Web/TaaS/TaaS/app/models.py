from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg_to = db.Column(db.Text)
    msg_from = db.Column(db.Text)
    message = db.Column(db.Text)