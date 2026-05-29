from app.extensions import db
from app.models.base import BaseModel
from flask_login import UserMixin

# User model
class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    phones = db.relationship('UserPhone', backref='user', lazy=True, cascade='all, delete-orphan')
    emails = db.relationship('UserEmail', backref='user', lazy=True, cascade='all, delete-orphan')

class UserPhone(BaseModel):
    __tablename__ = 'user_phone'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class UserEmail(BaseModel):
    __tablename__ = 'user_email'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)