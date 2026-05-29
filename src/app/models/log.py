from app.extensions import db
from app.models.base import BaseModel

class Logs(BaseModel):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    target_entity = db.Column(db.String(50), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(20), nullable=False)