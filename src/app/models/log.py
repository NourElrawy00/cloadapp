import enum
from app.extensions import db
from app.models.base import BaseModel


class LogAction(enum.Enum):
    create  = 'create'
    update  = 'update'
    delete  = 'delete'
    restore = 'restore'


class LogEntity(enum.Enum):
    user           = 'user'
    product        = 'product'
    client         = 'client'
    client_agent   = 'client_agent'
    supplier       = 'supplier'
    buy            = 'buy'
    delivery       = 'delivery'
    invoice        = 'invoice'
    payment        = 'payment'
    offer          = 'offer'
    warehouse      = 'warehouse'
    warehouse_item = 'warehouse_item'


class Logs(BaseModel):
    __tablename__ = 'log'

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    action        = db.Column(db.Enum(LogAction),  nullable=False)
    target_entity = db.Column(db.Enum(LogEntity),  nullable=False, index=True)
    target_id     = db.Column(db.Integer,           nullable=False, index=True)
    diff          = db.Column(db.JSON,              nullable=True)

    user = db.relationship('User', backref='logs', lazy=True)